# Custom nodes for ComfyUI

## Microsoft kosmos-2 for Comfyui

An implementation of [Microsoft kosmos-2](https://huggingface.co/microsoft/kosmos-2-patch14-224) image to text transformer

![](img/ComfyUI_00001_.png)

This node takes a prompt that can influence the ouput, for example, if you put "Very detailed, an image of", it outputs more details than just "An image of". kosmos-2 is quite impressive, it recognizes famous people and written text in the image:

![](img/ComfyUI_00132.jpg)
kosmos-2 output of the above (unpixelated) image: _An image of Ivanka Trump standing next to a tombstone that says Donald Trump, with a crowd of people standing behind her._

**At the first start, the kosmos-2 model files will be downloaded from huggingface.**

### Examples:

<table>
    <tr>
        <td><img src="img/00049-2467344372.jpg" width="250"></td>
        <td>
            <b>Prompt:</b> An image of<br>
            <b>Output</b><br>
            Description: An image of a tent and lantern under a beautiful sunset.<br>
            Keywords: a tent,lantern,a beautiful sunset<p>
        </td>
    </tr>
    <tr>
        <td><img src="img/2023-12-05_18-14-17_8435.jpg" width="250"></td>
        <td>
            <b>Prompt:</b> An image of<br>
            <b>Output</b><br>
            Description: An image of a man eating a plate of food with a monster eating it out of his mouth.<br>
            Keywords: a man,a plate of food,a monster,his mouth<p><p>
            <b>Prompt:</b> A very detailed description of<br>
            <b>Output</b><br>
            Description: A very detailed description of the food in the plate, the man is eating a large piece of meat, while the monster is devouring the food.<br>
            Keywords: the plate,the man,a large piece of meat,the monster,the food<p>
        </td>
    </tr>
    <tr>
        <td><img src="img/2023-12-26-191725_546.jpg" width="250"></td>
        <td>
            <b>Prompt:</b> An image of<br>
            <b>Output</b><br>
            Description: An image of a beautiful woman in a medieval dress.<br>
            Keywords: a beautiful woman in a medieval dress<p><p>
            <b>Prompt:</b> A woman doing<br>
            <b>Output</b><br>
            Description: A woman doing a striptease in a field of flowers.<br>
            Keywords: a field of flowers<p>
            <b>Prompt:</b> The background of this image<br>
            <b>Output</b><br>
            Description: The background of this image is a beautiful countryside scene with a woman standing in a field wearing a black and blue dress.<br>
            Keywords: a woman,a field,a black and blue dress
        </td>
    </tr>
    <tr>
        <td><img src="img/road-sign-3425675009.jpg" width="250"></td>
        <td>
            <b>Prompt:</b> This image shows<br>
            <b>Output</b><br>
            Description: This image shows a road sign and a traffic sign in the woods.<br>
            Keywords: a road sign<p>
        </td>
    </tr>
    <tr>
        <td><img src="img/35_727584-2581741032.jpg" width="250"></td>
        <td>
            <b>Prompt:</b> (none)<br>
            <b>Output</b><br>
            Description: The flyer for the opening of the semester.<br>
            Keywords: The flyer for the opening of the semester<p>
        </td>
    </tr>
</table>

----

## Save Image w/o Metadata

![](img/workflow.png)

With this save image node, you can include or exclude the ComfyUI workflow and/or extra pgn-info metadata. It is a derivation of ComfyUI's original save image node.

----

## Installation

Unzip or git clone this repository into ComfyUI/custom_nodes folder and restart ComfyUI.
