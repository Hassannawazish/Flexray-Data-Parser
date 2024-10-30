import logging
from readers.labelled_data_reader import A2D2DatasetIterator
from data_models import DynamicVehicleData
from helpers.logging_helper import configure_logging

def get_dynamic_vehicle_data_dict(flexray_data):
    """
    Creates a dictionary of dynamic vehicle data from FlexRayData.

    Args:
        flexray_data (FlexRayData): The FlexRay data for a specific frame.

    Returns:
        dict: A dictionary containing all dynamic vehicle data.
    """
    data_dict = {
        "frame_name": flexray_data.frame_name,
        "timestamp": flexray_data.timestamp,
        "dynamic_data": {}
    }

    # Populate dynamic data fields
    for param, data in flexray_data.__dict__.items():
        if isinstance(data, DynamicVehicleData):
            data_dict["dynamic_data"][param] = {
                "timestamps": data.timestamps,
                "values": data.values,
                "unit": data.unit
            }
    return data_dict

def main(label_file: str, flexray_file: str):
    """
    Main function to process A2D2 dataset with specified label and FlexRay files.
    """
    configure_logging()  # Use the centralized logging configuration
    logging.info("Starting dataset processing...")

    try:
        dataset = A2D2DatasetIterator(label_file, flexray_file)
        logging.debug("Dataset iterator created successfully.")

        while True:
            record = dataset.step_next()
            if record is None:
                logging.info("No more records to process.")
                break

            logging.info(f"Image Name: {record.image_data.name}")
            logging.info(f"Bounding Boxes: {record.image_data.boxes}")

            # If FlexRay data exists, format and log it as a single dictionary
            if record.flexray_data:
                flexray_data_dict = get_dynamic_vehicle_data_dict(record.flexray_data)
                logging.info(f"FlexRay Data: {flexray_data_dict}")
            else:
                logging.warning("FlexRay data not found for this record.")

    except Exception as e:
        logging.error(f"Error processing dataset: {str(e)}")

    logging.info("Dataset processing completed.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        logging.error("Usage: python main.py <path_to_3d_labels_json> <path_to_flexray_data_json>")
    else:
        label_file = sys.argv[1]
        flexray_file = sys.argv[2]
        main(label_file, flexray_file)
