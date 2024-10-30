# a2d2_dataset/readers/flexray_data_reader.py

import json
import logging
from utils.validators import validate_3d_labels, validate_flexray_data
from data_models import ImageData, FlexRayData, DynamicVehicleData

def load_3d_labels(file_path: str) -> list:
    """
    Loads 3D label data from a JSON file and validates it.
    """
    logger = logging.getLogger("load_3d_labels")
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        validate_3d_labels(data)
        images = [ImageData(**img_data) for img_data in data["images"]]
        return images
    except Exception as e:
        logger.error(f"Failed to load 3D labels: {e}")
        raise

def load_flexray_data(file_path: str) -> list:
    """
    Loads FlexRay data from a JSON file and validates it.
    """
    logger = logging.getLogger("load_flexray_data")
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        validate_flexray_data(data)

        # Check if data is nested under a "flexray" key in each entry
        flexray_data = []
        for entry in data:
            if "flexray" in entry:
                # Unpack the "flexray" key contents and parse into FlexRayData
                flexray_entry = entry["flexray"]
                flexray_data.append(FlexRayData(
                    frame_name=entry["frame_name"],
                    timestamp=entry["timestamp"],
                    acceleration_x=DynamicVehicleData(**flexray_entry["acceleration_x"]),
                    acceleration_y=DynamicVehicleData(**flexray_entry["acceleration_y"]),
                    acceleration_z=DynamicVehicleData(**flexray_entry["acceleration_z"]),
                    accelerator_pedal=DynamicVehicleData(**flexray_entry["accelerator_pedal"]),
                    accelerator_pedal_gradient_sign=DynamicVehicleData(**flexray_entry["accelerator_pedal_gradient_sign"]),
                    angular_velocity_omega_x=DynamicVehicleData(**flexray_entry["angular_velocity_omega_x"]),
                    angular_velocity_omega_y=DynamicVehicleData(**flexray_entry["angular_velocity_omega_y"]),
                    angular_velocity_omega_z=DynamicVehicleData(**flexray_entry["angular_velocity_omega_z"]),
                    brake_pressure=DynamicVehicleData(**flexray_entry["brake_pressure"]),
                    distance_pulse_front_left=DynamicVehicleData(**flexray_entry["distance_pulse_front_left"]),
                    distance_pulse_front_right=DynamicVehicleData(**flexray_entry["distance_pulse_front_right"]),
                    distance_pulse_rear_left=DynamicVehicleData(**flexray_entry["distance_pulse_rear_left"]),
                    distance_pulse_rear_right=DynamicVehicleData(**flexray_entry["distance_pulse_rear_right"]),
                    driving_direction=DynamicVehicleData(**flexray_entry["driving_direction"]),
                    gear=DynamicVehicleData(**flexray_entry["gear"]),
                    latitude_degree=DynamicVehicleData(**flexray_entry["latitude_degree"]),
                    latitude_direction=DynamicVehicleData(**flexray_entry["latitude_direction"]),
                    longitude_degree=DynamicVehicleData(**flexray_entry["longitude_degree"]),
                    longitude_direction=DynamicVehicleData(**flexray_entry["longitude_direction"]),
                    pitch_angle=DynamicVehicleData(**flexray_entry["pitch_angle"]),
                    roll_angle=DynamicVehicleData(**flexray_entry["roll_angle"]),
                    steering_angle=DynamicVehicleData(**flexray_entry["steering_angle"]),
                    steering_angle_calculated=DynamicVehicleData(**flexray_entry["steering_angle_calculated"]),
                    steering_angle_calculated_sign=DynamicVehicleData(**flexray_entry["steering_angle_calculated_sign"]),
                    steering_angle_sign=DynamicVehicleData(**flexray_entry["steering_angle_sign"]),
                    vehicle_speed=DynamicVehicleData(**flexray_entry["vehicle_speed"])
                ))
            else:
                logger.error(f"Expected 'flexray' key in entry: {entry}")
        return flexray_data

    except Exception as e:
        logger.error(f"Failed to load FlexRay data: {e}")
        raise