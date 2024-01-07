from nodes import SaveImage
import folder_paths
import random

class SaveImage_NoWorkflow(SaveImage):
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(s):
        return {"required": 
                    {"images": ("IMAGE", ), "filename_prefix": ("STRING", {"default": "ComfyUI"}),
                    "save_image": ("BOOLEAN", {"default": True}),
                    "include_prompt": ("BOOLEAN", {"default": True}),
                    "include_workflow": ("BOOLEAN", {"default": True}),
                    },
                    
                "hidden": 
                    {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
                }

    RETURN_TYPES = ()
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = "Hangover"

    def save_images(self, images, filename_prefix="ComfyUI", save_image = False, include_prompt=False, include_workflow=False, prompt=None, extra_pnginfo=None):
        if not include_prompt:
            prompt = None
        if not include_workflow:
            extra_pnginfo = None

        if save_image:
            self.__init__()
        else:
            self.output_dir = folder_paths.get_temp_directory()
            self.type = "temp"
            self.prefix_append = "_temp_" + ''.join(random.choice("abcdefghijklmnopqrstupvxyz") for x in range(5))
            self.compress_level = 1

        return(super().save_images(images, filename_prefix, prompt, extra_pnginfo))
