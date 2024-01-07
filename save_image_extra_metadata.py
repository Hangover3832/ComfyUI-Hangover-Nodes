from nodes import SaveImage

class SaveImage_NoWorkflow(SaveImage):
    @classmethod
    def INPUT_TYPES(s):
        return {"required": 
                    {"images": ("IMAGE", ), "filename_prefix": ("STRING", {"default": "ComfyUI"}),
                    "include_prompt": ("BOOLEAN", {"default": "false"}),
                    "include_workflow": ("BOOLEAN", {"default": "false"}),
                    },
                    
                "hidden": 
                    {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
                }

    RETURN_TYPES = ()
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = "Hangover"

    def save_images(self, images, filename_prefix="ComfyUI", include_prompt=False, include_extra_pnginfo=False, prompt=None, extra_pnginfo=None):
        if not include_prompt:
            prompt = None
        if not include_extra_pnginfo:
            extra_pnginfo = None
        return(super().save_images(images, filename_prefix, prompt, extra_pnginfo))
