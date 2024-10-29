# a2d2_dataset/main.py

import logging
from dataset import A2D2DatasetIterator

def format_accel_data(accel_data):
    """
    Formats the acceleration data to the desired string format.
    
    Args:
        accel_data (AccelerationData): The acceleration data to format.

    Returns:
        str: Formatted acceleration data as a string.
    """
    return f"[timestamps={accel_data.timestamps}, values={accel_data.values}, unit='{accel_data.unit}']"

def main(label_file: str, flexray_file: str):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )

    logging.info("Starting dataset processing...")
    try:
        dataset = A2D2DatasetIterator(label_file, flexray_file)

        # Step through each timestamp and retrieve matched data
        while True:
            record = dataset.step_next()
            if record is None:
                break

            logging.info(f"Image Name: {record.image_data.name}")
            logging.info(f"Bounding Boxes: {record.image_data.boxes}")
            if record.flexray_data:
                logging.info(f"FlexRay Data: frame_name='{record.flexray_data.frame_name}', "
                             f"timestamp={record.flexray_data.timestamp}, "
                             f"acceleration_x={format_accel_data(record.flexray_data.acceleration_x)}, "
                             f"acceleration_y={format_accel_data(record.flexray_data.acceleration_y)}")

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
