# a2d2_dataset/json_parser.py

import json
from data_models import ImageData, Box3D, Box3DAttributes, FlexRayData, DynamicVehicleData

def load_3d_labels(file_path: str) -> list:
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

def load_flexray_data(file_path: str) -> list:
    """
    Loads FlexRay data from a JSON file.
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    flexray_data = [
        FlexRayData(
            frame_name=entry["frame_name"],
            timestamp=entry["timestamp"],
            acceleration_x=DynamicVehicleData(**entry["flexray"]["acceleration_x"]),
            acceleration_y=DynamicVehicleData(**entry["flexray"]["acceleration_y"]),
            acceleration_z=DynamicVehicleData(**entry["flexray"]["acceleration_z"]),
            accelerator_pedal=DynamicVehicleData(**entry["flexray"]["accelerator_pedal"]),
            accelerator_pedal_gradient_sign=DynamicVehicleData(**entry["flexray"]["accelerator_pedal_gradient_sign"]),
            angular_velocity_omega_x=DynamicVehicleData(**entry["flexray"]["angular_velocity_omega_x"]),
            angular_velocity_omega_y=DynamicVehicleData(**entry["flexray"]["angular_velocity_omega_y"]),
            angular_velocity_omega_z=DynamicVehicleData(**entry["flexray"]["angular_velocity_omega_z"]),
            brake_pressure=DynamicVehicleData(**entry["flexray"]["brake_pressure"]),
            distance_pulse_front_left=DynamicVehicleData(**entry["flexray"]["distance_pulse_front_left"]),
            distance_pulse_front_right=DynamicVehicleData(**entry["flexray"]["distance_pulse_front_right"]),
            distance_pulse_rear_left=DynamicVehicleData(**entry["flexray"]["distance_pulse_rear_left"]),
            distance_pulse_rear_right=DynamicVehicleData(**entry["flexray"]["distance_pulse_rear_right"]),
            driving_direction=DynamicVehicleData(**entry["flexray"]["driving_direction"]),
            gear=DynamicVehicleData(**entry["flexray"]["gear"]),
            latitude_degree=DynamicVehicleData(**entry["flexray"]["latitude_degree"]),
            latitude_direction=DynamicVehicleData(**entry["flexray"]["latitude_direction"]),
            longitude_degree=DynamicVehicleData(**entry["flexray"]["longitude_degree"]),
            longitude_direction=DynamicVehicleData(**entry["flexray"]["longitude_direction"]),
            pitch_angle=DynamicVehicleData(**entry["flexray"]["pitch_angle"]),
            roll_angle=DynamicVehicleData(**entry["flexray"]["roll_angle"]),
            steering_angle=DynamicVehicleData(**entry["flexray"]["steering_angle"]),
            steering_angle_calculated=DynamicVehicleData(**entry["flexray"]["steering_angle_calculated"]),
            steering_angle_calculated_sign=DynamicVehicleData(**entry["flexray"]["steering_angle_calculated_sign"]),
            steering_angle_sign=DynamicVehicleData(**entry["flexray"]["steering_angle_sign"]),
            vehicle_speed=DynamicVehicleData(**entry["flexray"]["vehicle_speed"])
        )
        for entry in data
    ]
    return flexray_data
