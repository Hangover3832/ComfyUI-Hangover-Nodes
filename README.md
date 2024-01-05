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
<p>
<h3>Examples:</h3>
<table>
    <tr>
        <td><img src="img/00049-2467344372.jpg" width="250"></td>
        <td>
            Prompt: An image of<br>
            Output:<br>
            Description: An image of a tent and lantern under a beautiful sunset.<br>
            Keywords: a tent,lantern,a beautiful sunset<p>
        </td>
    </tr>
    <tr>
        <td><img src="img/2023-12-05_18-14-17_8435.jpg" width="250"></td>
        <td>
            Prompt: An image of<br>
            Output:<br>
            Description: An image of a man eating a plate of food with a monster eating it out of his mouth.<br>
            Keywords: a man,a plate of food,a monster,his mouth
            <p>
            Prompt: A very detailed description of<br>
            Output:<br>
            Description: A very detailed description of the food in the plate, the man is eating a large piece of meat, while the monster is devouring the food.<br>
            Keywords: the plate,the man,a large piece of meat,the monster,the food<p>
        </td>
    </tr>
    <tr>
        <td><img src="img/2023-12-26-191725_546.jpg" width="250"></td>
        <td>
            Prompt: An image of<br>
            Output:<br>
            Description: An image of a beautiful woman in a medieval dress.<br>
            Keywords: a beautiful woman in a medieval dress
            <p>
            Prompt: A woman doing<br>
            Output:<br>
            Description: A woman doing a striptease in a field of flowers.<br>
            Keywords: a field of flowers
            <p>
            Prompt: The background of this image<br>
            Output:<br>
            Description: The background of this image is a beautiful countryside scene with a woman standing in a field wearing a black and blue dress.<br>
            Keywords: a woman,a field,a black and blue dress
        </td>
    </tr>
    <tr>
        <td><img src="img/road-sign-3425675009.jpg" width="250"></td>
        <td>
            Prompt: This image shows<br>
            Output:<br>
            Description: This image shows a road sign and a traffic sign in the woods.<br>
            Keywords: a road sign<p>
        </td>
    </tr>
    <tr>
        <td><img src="img/35_727584-2581741032.jpg" width="250"></td>
        <td>
            Prompt:<br>
            Output:<br>
            Description: The flyer for the opening of the semester.<br>
            Keywords: The flyer for the opening of the semester<p>
        </td>
    </tr>
</table>

<hr>

<h2>Installation</h2>

Unzip or git clone this repository into ComfyUI/custom_nodes folder and restart ComfyUI.