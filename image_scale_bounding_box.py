from nodes import ImageScale, MAX_RESOLUTION
import comfy.utils


class ImageScaleBoundingBox:

    upscale_methods = ["nearest-exact", "bilinear", "area", "bicubic", "lanczos"]
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "upscale"
    CATEGORY = "Hangover"

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "image": ("IMAGE",),
                    "upscale_method": (s.upscale_methods,),
                    "box_width": ("INT", {"default": 512, "min": 1, "max": MAX_RESOLUTION, "step": 1}),
                    "box_height": ("INT", {"default": 512, "min": 1, "max": MAX_RESOLUTION, "step": 1})}}

    def upscale(self, image, upscale_method, box_width, box_height):
        samples = image.movedim(-1,1)
        w = round(samples.shape[3])
        h = round(samples.shape[2])
        scale_by = min(box_width/w, box_height/h)
        new_width = round(w * scale_by)
        new_height = round(h * scale_by)
        s = comfy.utils.common_upscale(samples, new_width, new_height, upscale_method, "disabled")
        s = s.movedim(1,-1)
        return (s,)
