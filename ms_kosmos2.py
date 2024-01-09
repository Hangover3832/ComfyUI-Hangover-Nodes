'''
An implementation of Microsoft kosmos-2 image to text transformer.
https://huggingface.co/microsoft/kosmos-2-patch14-224

ToDo: Output bboxes and/or masks

https://github.com/Hangover3832

Alex
'''

from PIL import Image
from transformers import AutoProcessor, AutoModelForVision2Seq, Kosmos2Config
import torchvision.transforms as T
import numpy as np

class MsKosmos2:
    HUGGINGFACE_MODEL_NAMES = ["microsoft/kosmos-2-patch14-224"] # other/newer models can be added here

    def __init__(self):
        self.prefix = "<grounding> "
        self.model = None
        self.processor = None
        self.modelname = ""

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "prompt": ("STRING", {"multiline": False, "default": "An image of"},),
                "huggingface_model": (MsKosmos2.HUGGINGFACE_MODEL_NAMES,{"default": MsKosmos2.HUGGINGFACE_MODEL_NAMES[0]},)
            }
        }

    # RETURN_TYPES = ("STRING", "STRING", "BBOX", "MASK")
    # RETURN_NAMES = ("description","keywords","bboxes", masks)
    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("description", "keywords",)
    FUNCTION = "interrogate"
    OUTPUT_NODE = False
    CATEGORY = "Hangover"

    def interrogate(self, image, prompt, huggingface_model):

        if (self.model == None) or (self.processor == None) or (self.modelname != huggingface_model):
            print(f"kosmos2: loading model {huggingface_model}, please stand by....")
            self.model = AutoModelForVision2Seq.from_pretrained(huggingface_model)
            self.processor = AutoProcessor.from_pretrained(huggingface_model)
            self.modelname = huggingface_model

        descriptions = ""
        entity_str = ""
        # bboxlist = []
        for im in image:
            i = 255. * im.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            inputs = self.processor(text=self.prefix+prompt, images=img, return_tensors="pt")
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
            # By default, the generated  text is cleanup and the entities are extracted.
            description, entities = self.processor.post_process_generation(generated_text)
            # entities = [('a snowman', (12, 21), [(0.390625, 0.046875, 0.984375, 0.828125)]), ('a fire', (41, 47), [(0.171875, 0.015625, 0.484375, 0.890625)])]

            descriptions += description + '\n'
            elist = []
            for entity_name, (start, end), bbox in entities:
                '''
                bbx = bbox[0]
                b = (round(bbx[0] * img.width),
                    round(bbx[1] * img.height),
                    round((bbx[2] - bbx[0]) * img.width),
                    round((bbx[3] - bbx[1]) * img.height)
                )
                bbxlist.append(b)
                '''
                elist.append(entity_name)

            entity_str += ",".join(elist)
            entity_str += '\n'
            # bboxlist.append(bbxlist)

        return (descriptions, entity_str,)
