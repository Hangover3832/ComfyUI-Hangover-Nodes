# Custom nodes for ComfyUI

[ComfyUI](https://github.com/comfyanonymous/ComfyUI) is the awsome stable diffusion GUI and backend.

**Pleane note that this repository is currently a work in progress and might change anytime.**

## Nodes:
- Kosmos-2: Grounding Multimodal Large Language Models to the World 
- Save Image with or wothout Metadata
- Scale an Image To A Bounding Box

### Node: Microsoft kosmos-2 for Comfyui

An implementation of [Microsoft kosmos-2](https://huggingface.co/microsoft/kosmos-2-patch14-224) image to text transformer

![](img/ComfyUI_00001_.png)

This node takes a prompt that can influence the ouput, for example, if you put "Very detailed, an image of", it outputs more details than just "An image of". kosmos-2 is quite impressive, it recognizes famous people and written text in the image:

![Alt text](img/th-406341032.jpg) \
_**kosmos-2 output:** An image of Donald Trump giving the peace sign with the words "Make America Great Again" written next to him._

**At the first start, the kosmos-2 model files will be downloaded from huggingface. Please be patient.**

[See example outputs and workflows](examples/examples.md)

----

### Node: Save Image w/o Metadata

![](img/workflow.png)

With this custom save image node, you can include or exclude the prompt and/or the ComfyUI workflow metadata in the saved image. It is a derivation of ComfyUI's builtin save image node.

---

### Node: Scale Image To Bounding Box
This node scales an input image to a given box size whereby the aspect ratio keeps retained.

---

## Installation

Unzip or git clone this repository into ComfyUI/custom_nodes folder and restart ComfyUI.
