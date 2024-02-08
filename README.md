# Custom nodes for ComfyUI

[ComfyUI](https://github.com/comfyanonymous/ComfyUI) is the awesome stable diffusion GUI and backend.

**Please note that this repository is currently a (learning) work in progress and might change anytime.** It has been tested in Windows 10 only so far.

## Updates

* Save Image now has only 1 button to include/exclude metadata. You now can disable saving the image, thus it acts as an image preview only. Note that you can still save the image, by right clicking on it, that will include or exclude the workflow according to the setting.
* kosmos-2 interrogator now outputs a mask indicating the recognized elements in the image.
* "Image Scale To Bounding Box" now can pad the image to its given box size ([examples](examples/examples.md)).
* New node: Make inpainting model.
* Kosmos-2 update: Ability to strip out the prompt from the response (credit to za-wa-n-go).

## Nodes overview:

- Kosmos-2: Grounding Multimodal Large Language Models to the World
- Stable Diffusion Privacy: Save Image with or without Metadata
- Scale an Image To A Bounding Box
- Easily make an inpainting version of any SD1.5 model

---

### Node: Microsoft kosmos-2 for ComfyUI

An implementation of [Microsoft kosmos-2](https://huggingface.co/microsoft/kosmos-2-patch14-224) text & image to text transformer .

![](img/ComfyUI_00001_.png)

This node takes a prompt that can influence the output, for example, if you put "Very detailed, an image of", it outputs more details than just "An image of". kosmos-2 is quite impressive, it recognizes famous people and written text in the image:

![Alt text](img/th-406341032.jpg) \
_**kosmos-2 output:** An image of Donald Trump giving the peace sign with the words "Make America Great Again" written next to him._

**At the first start, the kosmos-2 model files will be downloaded from huggingface. Please be patient.** The model file is about 6GB in size. There is a cpu/gpu selector, but be aware that the model will eat up about 6GB of your precious VRAM in gpu mode!

[See example outputs and workflows](examples/examples.md)

Also see [Moondream](https://github.com/Hangover3832/ComfyUI-Hangover-Moondream)

---

### Node: Save Image w/o Metadata

![](img/workflow.png)
With this custom save image node, you can include or exclude the ComfyUI workflow metadata in the saved image. It is a derivation of ComfyUI's built-in save image node.

---

### Node: Scale Image To Bounding Box

This node scales an input image into a given box size, whereby the aspect ratio keeps retained. The image can also be padded to the full box size with an arbitrary color.

![Alt text](img/bounding_box.png)

[See example outputs and workflows](examples/examples.md)

---

### Node: Make Inpainting Model for SD1.5

![Alt text](img/make_inpaint_model.PNG)
This node easy creates an inpainting version of any SD1.5 model on the fly. No need to have GB's of inpainting models laying on your drive. This is very useful for any kind of inpainting nodes like detailers. Make sure you have the original SD1.5 models from [RunwayML](https://huggingface.co/runwayml) in your models folder:

- [v1-5-pruned-emaonly.ckpt](https://huggingface.co/runwayml/stable-diffusion-v1-5/blob/main/v1-5-pruned-emaonly.ckpt) or[v1-5-pruned-emaonly.safetensors](https://huggingface.co/runwayml/stable-diffusion-v1-5/blob/main/v1-5-pruned-emaonly.safetensors)
- [sd-v1-5-inpainting.ckpt](https://huggingface.co/runwayml/stable-diffusion-inpainting/blob/main/sd-v1-5-inpainting.ckpt)

They are needed for the calculation.

[See examples](examples/examples.md)

---

## Installation

Unzip or git clone this repository into ComfyUI/custom_nodes folder and restart ComfyUI.
