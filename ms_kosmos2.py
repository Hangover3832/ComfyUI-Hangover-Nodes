'''
An implementation of Microsoft kosmos-2 image to text transformer.
https://huggingface.co/microsoft/kosmos-2-patch14-224

https://github.com/Hangover3832

Alex
'''

from PIL import Image
from transformers import AutoProcessor, AutoModelForVision2Seq
import torchvision.transforms as T
import numpy as np
import gc
import torch
from comfy_extras.nodes_mask import MaskComposite


class MsKosmos2:
    HUGGINGFACE_MODEL_NAMES = ["microsoft/kosmos-2-patch14-224"] # other/newer models can be added here
    DEVICES = ["cpu", "gpu"] if torch.cuda.is_available() else  ["cpu"]

    def __init__(self):
        self.prefix = "<grounding> "
        self.model = None
        self.processor = None
        self.modelname = ""
        self.device = ""

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "prompt": ("STRING", {"multiline": False, "default": "An image of"},),
                "huggingface_model": (MsKosmos2.HUGGINGFACE_MODEL_NAMES, {"default": MsKosmos2.HUGGINGFACE_MODEL_NAMES[0]},),
                "device": (MsKosmos2.DEVICES, {"default": MsKosmos2.DEVICES[0]},),
                "strip_prompt": ("BOOLEAN", {"default": True},),
            }
        }

    # RETURN_TYPES = ("STRING", "STRING", "BBOX", "MASK")
    # RETURN_NAMES = ("description","keywords","bboxes", masks)
    RETURN_TYPES = ("STRING", "STRING", "MASK",)
    RETURN_NAMES = ("description", "keywords", "mask",)
    FUNCTION = "interrogate"
    OUTPUT_NODE = False
    CATEGORY = "Hangover"

    def interrogate(self, image, prompt, huggingface_model, device, strip_prompt):
        dev = "cuda" if device == "gpu" else "cpu"
        if (self.model == None) or (self.processor == None) or (self.modelname != huggingface_model) or (device != self.device):
            del self.model
            del self.processor
            gc.collect()
            if (device == "cpu") and torch.cuda.is_available():
                torch.cuda.empty_cache()
            print(f"kosmos2: loading model {huggingface_model}, please stand by....")
            self.model = AutoModelForVision2Seq.from_pretrained(huggingface_model).to(dev)
            self.processor = AutoProcessor.from_pretrained(huggingface_model)
            self.modelname = huggingface_model
            self.device = device

        descriptions = ""
        entity_str = ""
        width = round(image.shape[2])
        height = round(image.shape[1])
        mask = torch.full((1, height, width), 0., dtype=torch.float32, device="cpu")

        for im in image:
            i = 255. * im.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            
            # generate text
            prompt_full = self.prefix + prompt

            inputs = self.processor(text=prompt_full, images=img, return_tensors="pt").to(dev)
            generated_ids = self.model.generate(
                pixel_values=inputs["pixel_values"],
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                image_embeds=None,
                image_embeds_position_mask=inputs["image_embeds_position_mask"],
                use_cache=True,
                max_new_tokens=128,
            )
            generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

            # delete prompt
            if strip_prompt == True:
                generated_text = generated_text.replace(prompt_full, '').strip()

            # By default, the generated text is cleanup and the entities are extracted.
            description, entities = self.processor.post_process_generation(generated_text)
            # entities = [('a snowman', (12, 21), [(0.390625, 0.046875, 0.984375, 0.828125)]), ('a fire', (41, 47), [(0.171875, 0.015625, 0.484375, 0.890625)])]
            descriptions += description + '\n'

            elist = []
            for entity_name, (start, end), bbox in entities:
                bbx = bbox[0]
                x = round(bbx[0] * width)
                y = round(bbx[1] * height)
                w = round((bbx[2] - bbx[0]) * width)
                h = round((bbx[3] - bbx[1]) * height)
                print(x, y, w, h)
                m = torch.full((1, h, w), 1., dtype=torch.float32, device="cpu")
                mask = MaskComposite.combine(self, mask, m, x, y, "or")[0]

                elist.append(entity_name)

            entity_str += ",".join(elist)
            entity_str += '\n'
            # bboxlist.append(bbxlist)

        return (descriptions, entity_str, mask,)
