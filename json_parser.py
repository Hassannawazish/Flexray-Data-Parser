# a2d2_dataset/parser.py

import json
from data_models import ImageData, Box3D, Box3DAttributes, FlexRayData

def load_3d_labels(file_path: str) -> ImageData:
    """
    Loads the 3D label data from a JSON file.
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    images = []
    for img_data in data["images"]:
        boxes = [
            Box3D(
                label=box["label"],
                occluded=box["occluded"],
                xtl=box["xtl"],
                ytl=box["ytl"],
                xbr=box["xbr"],
                ybr=box["ybr"],
                z_order=box["z_order"],
                attributes=Box3DAttributes.from_dict(box["attributes"])
            )
            for box in img_data["boxes"]
        ]
        images.append(ImageData(
            id=img_data["id"],
            name=img_data["name"],
            width=img_data["width"],
            height=img_data["height"],
            boxes=boxes
        ))
    return images

def load_flexray_data(file_path: str) -> FlexRayData:
    """
    Loads the FlexRay data from a JSON file.
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    flexray_data = [FlexRayData.from_dict(entry) for entry in data]
    return flexray_data
