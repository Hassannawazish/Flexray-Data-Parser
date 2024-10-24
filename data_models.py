# a2d2_dataset/data_models.py

from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class Box3DAttributes:
    """
    Represents the attributes of a 3D bounding box in an image.
    """
    tracking_id: int
    lane_id: int
    vechile_orientation: str
    indicator: str
    brake_lights: str
    vehicle_state: str
    alpha: float
    axis: List[float]
    center: List[float]
    size: List[float]
    truncation: float
    _class: str
    id: int
    occlusion: int
    rot_angle: float
    bbox_2d: List[float]
    points_3d: List[List[float]]

    @staticmethod
    def from_dict(attributes: Dict[str, Any]) -> 'Box3DAttributes':
        """
        Creates a Box3DAttributes object from a dictionary of attributes.
        """
        import json  # Importing json here to avoid unnecessary imports elsewhere
        return Box3DAttributes(
            tracking_id=attributes["tracking_id"],
            lane_id=attributes["lane_id"],
            vechile_orientation=attributes["vechile_orientation"],
            indicator=attributes["indicator"],
            brake_lights=attributes["brake_lights"],
            vehicle_state=attributes["vehicle_state"],
            alpha=attributes["alpha"],
            axis=json.loads(attributes["axis"]),
            center=json.loads(attributes["center"]),
            size=json.loads(attributes["size"]),
            truncation=attributes["truncation"],
            _class=attributes["class"],
            id=attributes["id"],
            occlusion=attributes["occlusion"],
            rot_angle=attributes["rot_angle"],
            bbox_2d=json.loads(attributes["2d_bbox"]),
            points_3d=json.loads(attributes["3d_points"])
        )

@dataclass
class Box3D:
    """
    Represents a single 3D bounding box in an image.
    """
    label: str
    occluded: int
    xtl: float
    ytl: float
    xbr: float
    ybr: float
    z_order: int
    attributes: Box3DAttributes

@dataclass
class ImageData:
    """
    Represents the image data with 3D bounding boxes.
    """
    id: str
    name: str
    width: int
    height: int
    boxes: List[Box3D] = field(default_factory=list)

@dataclass
class AccelerationData:
    """
    Represents acceleration data for a specific axis (x or y).
    """
    timestamps: List[int]
    values: List[float]
    unit: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'AccelerationData':
        """
        Creates an AccelerationData object from a dictionary.
        """
        return AccelerationData(
            timestamps=data["timestamps"],
            values=data["values"],
            unit=data["unit"]
        )

@dataclass
class FlexRayData:
    """
    Represents the flexray data for a specific frame.
    """
    frame_name: str
    timestamp: int
    acceleration_x: AccelerationData
    acceleration_y: AccelerationData

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'FlexRayData':
        """
        Creates a FlexRayData object from a dictionary.
        """
        return FlexRayData(
            frame_name=data["frame_name"],
            timestamp=data["timestamp"],
            acceleration_x=AccelerationData.from_dict(data["flexray"]["acceleration_x"]),
            acceleration_y=AccelerationData.from_dict(data["flexray"]["acceleration_y"])
        )

@dataclass
class Record:
    """
    Represents a full record including both the 3D labels and corresponding FlexRay data.
    """
    image_data: ImageData
    flexray_data: FlexRayData
