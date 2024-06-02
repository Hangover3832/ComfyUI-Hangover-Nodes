"""
@author: AlexL
@title: ComfyUI-Hangover-Image_Scale_Bouning_Box
@nickname: Hangover-Image_Scale_Bouning_Box
@description: Scales an input image into a given box size, whereby the aspect ratio keeps retained.
"""

from nodes import MAX_RESOLUTION
import comfy.utils
import torch.nn.functional as F
import torch


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
        w = image.shape[2]
        h = image.shape[1]
        scale_by = min(box_width/w, box_height/h)
        new_width = round(w * scale_by)
        new_height = round(h * scale_by)
        samples = comfy.utils.common_upscale(image.movedim(-1,1), new_width, new_height, upscale_method, "disabled").movedim(1,0)
        if padding in ImageScaleBoundingBox.PADDING:
            # if padding == "center":
            pad_left = (box_width - new_width) // 2
            pad_right = box_width - new_width - pad_left
            pad_top = (box_height - new_height) // 2
            pad_bottom = box_height - new_height - pad_top # ensure that we do not get any rounding error in the output image size
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
            pad = (pad_left, pad_right, pad_top, pad_bottom)

            r = ((pad_color & 0xFF0000) >> 16) / 255. # I know this & is not necessary, it's for readability
            g = ((pad_color & 0x00FF00) >> 8)  / 255.
            b = (pad_color & 0x0000FF) / 255.
            ir = F.pad(input=samples[0], pad=pad, mode='constant', value = r)
            ig = F.pad(input=samples[1], pad=pad, mode='constant', value = g)
            ib = F.pad(input=samples[2], pad=pad, mode='constant', value = b)
            samples = torch.stack([ir,ig,ib])

        samples = samples.movedim(0,-1)
        return (samples,)
