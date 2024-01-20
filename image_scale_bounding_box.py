from nodes import MAX_RESOLUTION
import comfy.utils
import torchvision.transforms.functional as F
from PIL import Image
import torch
import numpy as np


class ImageScaleBoundingBox:

    UPSCALE_METHOD = ["lanczos", "nearest-exact", "bilinear", "area", "bicubic"]
    PADDING = ["center", "top", "left", "right", "bottom"]
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "upscale"
    CATEGORY = "Hangover"

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "image": ("IMAGE",),
                    "upscale_method": (s.UPSCALE_METHOD,),
                    "box_width": ("INT", {"default": 512, "min": 1, "max": MAX_RESOLUTION, "step": 1}),
                    "box_height": ("INT", {"default": 512, "min": 1, "max": MAX_RESOLUTION, "step": 1}),
                    "padding": (["none"] + s.PADDING,),
                    "pad_color": ("INT", {"default": 0, "min": 0, "max": 0xFFFFFF, "step": 1, "display": "pad_color"}),
                    }
                }

    def upscale(self, image, upscale_method, box_width, box_height, padding, pad_color):
        samples = image.movedim(-1,1)
        w = samples.shape[3]
        h = samples.shape[2]
        scale_by = min(box_width/w, box_height/h)
        new_width = round(w * scale_by)
        new_height = round(h * scale_by)
        s = comfy.utils.common_upscale(samples, new_width, new_height, upscale_method, "disabled")
        s = s.movedim(1,-1)
        if padding in ImageScaleBoundingBox.PADDING:
            # in case padding == "center":
            pad_left = (box_width - new_width) // 2
            pad_right = box_width - new_width - pad_left
            pad_top = (box_height - new_height) // 2
            pad_bottom = box_height - new_height -pad_top # ensure that we do not get any rounding error in the output image size
            if padding == "top":
                pad_bottom = 0
                pad_top = box_height - new_height
            elif padding == "left":
                pad_right = 0
                pad_left = box_width - new_width
            elif padding == "right":
                pad_left = 0
                pad_right = box_width - new_width
            elif padding == "bottom":
                pad_top = 0
                pad_bottom = box_height - new_height

            i = Image.fromarray(np.clip(255. * s.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))
            r = (pad_color & 0xFF0000) >> 16 # I know this & is not necessary, it's for readability
            g = (pad_color & 0x00FF00) >> 8
            b = (pad_color & 0x0000FF)
            i = F.pad(img=i, padding=[pad_left, pad_top, pad_right, pad_bottom], fill=(r, g, b,), padding_mode="constant")
            s = torch.from_numpy(np.array(i).astype(np.float32) / 255.0).unsqueeze(0)

        return (s,)
