"""
@author: AlexL
@title: ComfyUI-Hangover-Kosmos2
@nickname: Hangover-ms_kosmos2
@description: An implementation of Microsoft kosmos-2 image to text transformer.
"""

# https://huggingface.co/microsoft/kosmos-2-patch14-224

# by https://github.com/Hangover3832


from PIL import Image
from transformers import AutoProcessor, AutoModelForVision2Seq
import numpy as np
import gc
import torch
from comfy_extras.nodes_mask import MaskComposite
from folder_paths import models_dir, folder_names_and_paths, add_model_folder_path, get_folder_paths, get_filename_list, get_full_path
import os

kosmos2_dir = "kosmos2"
huggingface_name = "microsoft/"
kosmos2_model_path = f"{models_dir}/{kosmos2_dir}"

try:
    if kosmos2_model_path not in get_folder_paths(kosmos2_dir):
        raise KeyError
except KeyError:
    add_model_folder_path(kosmos2_dir, kosmos2_model_path)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class MsKosmos2:
    MODEL_NAMES = ["kosmos-2-patch14-224"] # other/newer models can be added here
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
                "model": (s.MODEL_NAMES, {"default": s.MODEL_NAMES[0]},),
                "device": (s.DEVICES, {"default": s.DEVICES[0]},),
                "strip_prompt": ("BOOLEAN", {"default": True},),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "MASK",)
    RETURN_NAMES = ("description", "keywords", "mask",)
    FUNCTION = "interrogate"
    OUTPUT_NODE = False
    CATEGORY = "Hangover"

    def interrogate(self, image:torch.Tensor, prompt:str, model:str, device:str, strip_prompt:bool):
        dev = "cuda" if device.lower() == "gpu" else "cpu"
        model_paths = get_folder_paths(kosmos2_dir)

        # try to locate local model
        def model_in_path() -> str | None:
            for p in model_paths:
                result = f"{p}/{model}"
                if os.path.isdir(result):
                    return result
            return None
        model_path = model_in_path()

        if not model_path:
            # no local model, use huggingface hub
            model_path = f"{huggingface_name}{model}"

        if (self.model == None) or (self.processor == None) or (self.modelname != model) or (device != self.device):
            del self.model
            del self.processor
            gc.collect()
            if (device == "cpu") and torch.cuda.is_available():
                torch.cuda.empty_cache()
            print(f"kosmos2: loading model {model_path}, please stand by....")
            self.model = AutoModelForVision2Seq.from_pretrained(model_path).to(dev)
            self.processor = AutoProcessor.from_pretrained(model_path)
            self.modelname = model
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
                print(f"kosmos-2 entity '{entity_name}' at {x}, {y}, {w}, {h}")
                m = torch.full((1, h, w), 1., dtype=torch.float32, device="cpu")
                mask = MaskComposite.combine(self, mask, m, x, y, "or")[0]

                elist.append(entity_name)

            entity_str += ",".join(elist)
            entity_str += '\n'

        return (descriptions, entity_str, mask,)
