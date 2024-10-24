import logging
from dataset import A2D2Dataset

def log_all_boxes(record):
    """
    Logs all 3D boxes in the given record.
    
    Args:
        record (Record): The record containing the image data and 3D boxes.
    """
    if record.image_data.boxes:
        logging.info(f"Total number of 3D boxes in the image: {len(record.image_data.boxes)}")
        for idx, box in enumerate(record.image_data.boxes, start=1):
            logging.info(f"Box {idx}: {box}")
    else:
        logging.warning("No 3D boxes found in the record.")

def main(label_file: str, flexray_file: str):
    """
    Main function to load and process the A2D2 dataset.
    """
    # Setup logging configuration
    logging.basicConfig(
        level=logging.INFO,  # You can set it to logging.DEBUG for more verbose output
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()  # Outputs logs to the console
        ]
    )

    # Log the start of the process
    logging.info("Starting the A2D2 dataset processing...")

    try:
        dataset = A2D2Dataset(label_file, flexray_file)
        logging.info(f"Loaded 3D Labels: {dataset.get_3d_labels_size()} records")
        logging.info(f"Loaded FlexRay Data: {dataset.get_flexray_data_size()} records")

        # Access a specific record
        record = dataset.get_record("20181107132300_camera_frontcenter_000002775.png")

        # Log all the 3D boxes in the record
        log_all_boxes(record)

        # Log the FlexRay data for the record
        logging.info(f"FlexRay data: {record.flexray_data}")

    except Exception as e:
        logging.error(f"Error processing the dataset: {str(e)}")

    # Log the end of the process
    logging.info("Completed the A2D2 dataset processing.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        logging.error("Usage: python main.py <path_to_3d_labels_json> <path_to_flexray_data_json>")
    else:
        label_file = sys.argv[1]
        flexray_file = sys.argv[2]
        main(label_file, flexray_file)
