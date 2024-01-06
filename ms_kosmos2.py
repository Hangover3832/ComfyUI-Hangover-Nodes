'''
An implementation of Microsoft kosmos-2 image to text transformer.
https://huggingface.co/microsoft/kosmos-2-patch14-224

The generator also outputs a list of bboxes and correcponding keywords,
but I don't know how to handle lists of bboxes in comfyui.
Feel free to modify!

https://github.com/Hangover3832

Alex
'''

from PIL import Image
from transformers import AutoProcessor, AutoModelForVision2Seq
import torchvision.transforms as T
import numpy as np

model = AutoModelForVision2Seq.from_pretrained("microsoft/kosmos-2-patch14-224")
processor = AutoProcessor.from_pretrained("microsoft/kosmos-2-patch14-224")
# prompt = "<grounding>An image of"

class MsKosmos2:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "prompt": ("STRING", {
                    "multiline": False,
                    "default": "An image of"
                }),
            },
        }

    # RETURN_TYPES = ("STRING", "STRING","BBOX")
    # RETURN_NAMES = ("description","keywords","bboxes")
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("description","keywords")

    FUNCTION = "interrogate"
    #OUTPUT_NODE = False

    CATEGORY = "Custom"

    def interrogate(self, image, prompt):
        descriptionlist = []
        entitylist = []
        bboxlist = []
        for im in image:
            i = 255. * im.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            inputs = processor(text="<grounding>"+prompt, images=img, return_tensors="pt")
            generated_ids = model.generate(
                pixel_values=inputs["pixel_values"],
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                image_embeds=None,
                image_embeds_position_mask=inputs["image_embeds_position_mask"],
                use_cache=True,
                max_new_tokens=128,
            )
            generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            # By default, the generated  text is cleanup and the entities are extracted.
            description, entities = processor.post_process_generation(generated_text)
            # entities = [('a snowman', (12, 21), [(0.390625, 0.046875, 0.984375, 0.828125)]), ('a fire', (41, 47), [(0.171875, 0.015625, 0.484375, 0.890625)])]
            descriptionlist.append(description + '\n')

            entilist = []
            bbxlist = []
            for entity_name, (start, end), bbox in entities:
                bbx = bbox[0]
                b = (round(bbx[0] * img.width),
                    round(bbx[1] * img.height),
                    round((bbx[2] - bbx[0]) * img.width),
                    round((bbx[3] - bbx[1]) * img.height)
                )
                # print(entity_name,bbx,b)
                entilist.append(entity_name)
                bbxlist.append(b)

            entitylist.append(entilist)
            bboxlist.append(bbxlist)

        # print(descriptionlist)
        # print(entitylist)
        # print(bboxlist)

        # return (descriptionlist, entitylist, bboxlist,)
        return (descriptionlist, entitylist,)
