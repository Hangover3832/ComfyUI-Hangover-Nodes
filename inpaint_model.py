# from comfy_extras.nodes_model_merging import ModelAdd, ModelSubtract
import folder_paths
# import os
import comfy.sd

class MakeInpaintModel():

    V1_5_PRUNED = "Please select the original SD 1.5 pruned model"
    V1_5_INPAINT = "Please select the original SD 1.5 inpaint model"
    ckpts = folder_paths.get_filename_list("checkpoints")
    for f in ckpts:
        if "v1-5-pruned-emaonly." in f.lower():
            V1_5_PRUNED = f
        if "v1-5-inpainting." in f.lower():
            V1_5_INPAINT = f

    @classmethod
    def INPUT_TYPES(c):
        return {"required": {
                    "model": ("MODEL",),
                    "sd1_5_pruned": (c.ckpts,{"default": c.V1_5_PRUNED}),
                    "sd1_5_inpaint": (c.ckpts,{"default": c.V1_5_INPAINT}),
                    }
                }

    RETURN_TYPES = ("MODEL",)

    FUNCTION = "merge"
    OUTPUT_NODE = False
    CATEGORY = "Hangover"

    def merge(self, model, sd1_5_pruned, sd1_5_inpaint):
        '''
        add difference: result =  (sd1_5_inpaint - sd1_5_pruned) + model 
        '''
        ckpt_ip = folder_paths.get_full_path("checkpoints", sd1_5_inpaint)
        ckpt_pr = folder_paths.get_full_path("checkpoints", sd1_5_pruned)
        # load original sd1.5 inpaint model:
        ip = comfy.sd.load_checkpoint_guess_config(ckpt_ip, output_vae=False, output_clip=False, embedding_directory=folder_paths.get_folder_paths("embeddings"))[0]
        # load original sd1.5 pruned model
        pr = comfy.sd.load_checkpoint_guess_config(ckpt_pr, output_vae=False, output_clip=False, embedding_directory=folder_paths.get_folder_paths("embeddings"))[0]
        # subtract models (inpaint - pruned)
        kp = pr.get_key_patches("diffusion_model.")
        for k in kp:
            ip.add_patches({k: kp[k]}, -1.0, 1.0)

        # add the input model (diff + model)
        kp = model.clone().get_key_patches("diffusion_model.")
        for k in kp:
            ip.add_patches({k: kp[k]}, 1.0, 1.0)

        return(ip, )
