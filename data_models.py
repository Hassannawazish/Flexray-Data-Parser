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
class DynamicVehicleData:
    """
    Represents dynamic vehicle data (acceleration, steering angle, etc.) with timestamps and values.
    """
    timestamps: List[int]
    values: List[float]
    unit: str

@dataclass
class FlexRayData:
    """
    Represents the FlexRay data for a specific frame with various dynamic vehicle parameters.
    """
    frame_name: str
    timestamp: int
    acceleration_x: DynamicVehicleData
    acceleration_y: DynamicVehicleData
    acceleration_z: DynamicVehicleData
    accelerator_pedal: DynamicVehicleData
    accelerator_pedal_gradient_sign: DynamicVehicleData
    angular_velocity_omega_x: DynamicVehicleData
    angular_velocity_omega_y: DynamicVehicleData
    angular_velocity_omega_z: DynamicVehicleData
    brake_pressure: DynamicVehicleData
    distance_pulse_front_left: DynamicVehicleData
    distance_pulse_front_right: DynamicVehicleData
    distance_pulse_rear_left: DynamicVehicleData
    distance_pulse_rear_right: DynamicVehicleData
    driving_direction: DynamicVehicleData
    gear: DynamicVehicleData
    latitude_degree: DynamicVehicleData
    latitude_direction: DynamicVehicleData
    longitude_degree: DynamicVehicleData
    longitude_direction: DynamicVehicleData
    pitch_angle: DynamicVehicleData
    roll_angle: DynamicVehicleData
    steering_angle: DynamicVehicleData
    steering_angle_calculated: DynamicVehicleData
    steering_angle_calculated_sign: DynamicVehicleData
    steering_angle_sign: DynamicVehicleData
    vehicle_speed: DynamicVehicleData

@dataclass
class Record:
    """
    Represents a full record including both the 3D labels and corresponding FlexRay data.
    """
    image_data: ImageData
    flexray_data: FlexRayData
