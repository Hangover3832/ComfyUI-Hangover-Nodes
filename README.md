<h1>Custom nodes for ComfyUI</h1>
<hr>
<h2>Microsoft kosmos-2 for Comfyui</h2>

An implementation of Microsoft kosmos-2 image to text transformer.<br>
https://huggingface.co/microsoft/kosmos-2-patch14-224

<img src="img/ComfyUI_00001_.png">

This node takes a prompt that can influence the ouput, for example, if you put "Very detailed, an image of", it outputs more details than just "An image of". kosmos-2 is quite impressive, it recognizes famous people and written text in the image:<br>
<img src="img/ComfyUI_00132.jpg" width="400"><br>
kosmos-2 output of the above (unpixelated) image: "An image of Ivanka Trump standing next to a tombstone that says Donald Trump, with a crowd of people standing behind her."

<p>On the first start, the kosmos-2 model files will be downloaded from huggingface.

<hr>

<h2>Installation</h2>

Unzip or git clone this repository into ComfyUI/custom_nodes folder.