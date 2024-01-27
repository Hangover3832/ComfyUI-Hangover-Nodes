from .ms_kosmos2 import MsKosmos2
from .save_image_extra_metadata import SaveImage_NoWorkflow
from .image_scale_bounding_box import ImageScaleBoundingBox
from .inpaint_model import MakeInpaintModel


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "MS kosmos-2 Interrogator": MsKosmos2,
    "Save Image w/o Metadata" : SaveImage_NoWorkflow,
    "Image Scale Bounding Box" : ImageScaleBoundingBox,
    "Make Inpaint Model": MakeInpaintModel,
}
