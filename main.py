import logging
from dataset import A2D2DatasetIterator

def log_all_boxes(record):
    """
    Logs all 3D boxes in the given record.
    
    Args:
        record (Record): The record containing the image data and 3D boxes.
    """
    if record.image_data.boxes:
        logging.info(f"Total number of 3D boxes in the image '{record.image_data.name}': {len(record.image_data.boxes)}")
        for idx, box in enumerate(record.image_data.boxes, start=1):
            logging.info(f"Box {idx}: {box}")
    else:
        logging.warning(f"No 3D boxes found in the image '{record.image_data.name}'.")

def main(label_file: str, flexray_file: str):
    """
    Main function to load and process the A2D2 dataset.
    """
    # Setup logging configuration
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()  # Outputs logs to the console
        ]
    )

    # Log the start of the process
    logging.info("Starting the A2D2 dataset processing...")

    try:
        dataset = A2D2DatasetIterator(label_file, flexray_file)

        # Example of stepping through the dataset
        logging.info("Iterating through all images:")
        # while True:
        #     record = dataset.step_next()
        #     if record is None:
        #         break
        #     log_all_boxes(record)  # Log all 3D boxes in the current image
        #     logging.info(f"FlexRay data: {record.flexray_data}")

        first_record = dataset.step_next()
        if first_record:
            log_all_boxes(first_record)
            logging.info(f"FlexRay data: {first_record.flexray_data}")
        else:
            logging.warning("No data found in the dataset.")


        # Reset and access all data at once
        logging.info("Resetting dataset and fetching all records:")
        all_records = dataset.get_all_data()
        logging.info(f"Total number of records: {len(all_records)}")

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
