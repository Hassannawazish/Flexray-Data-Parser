from typing import Optional
from data_models import ImageData, FlexRayData, Record
from json_parser import load_3d_labels, load_flexray_data

class A2D2DatasetIterator:
    def __init__(self, label_file: str, flexray_file: str):
        """
        Initializes the dataset with paths to 3D label data and FlexRay data files.

        Args:
            label_file (str): Path to the 3D labels JSON file.
            flexray_file (str): Path to the FlexRay JSON file.
        """
        # Load the 3D label data and FlexRay data from their respective JSON files
        self.labels = load_3d_labels(label_file)  # List of ImageData
        self.flexray_data = load_flexray_data(flexray_file)  # List of FlexRayData
        self.index = 0  # Start index for iteration over dataset

    def __iter__(self):
        """
        Return the iterator object itself.
        """
        return self

    def __next__(self) -> Record:
        """
        Move to the next image record in the dataset.
        If the end of the dataset is reached, raises StopIteration.
        """
        if self.index >= len(self.labels):
            raise StopIteration  # Stop the iteration if index exceeds the length of the dataset
        image_data = self.labels[self.index]  # Get current image data
        flexray_data = self.match_flexray_data(image_data.name)  # Match FlexRay data for the current image
        self.index += 1  # Move to the next record
        return Record(image_data=image_data, flexray_data=flexray_data)

    def match_flexray_data(self, image_name: str) -> Optional[FlexRayData]:
        """
        Matches the FlexRay data with the given image name by comparing frame names.

        Args:
            image_name (str): Name of the image for which to find matching FlexRay data.

        Returns:
            Optional[FlexRayData]: The matching FlexRay data, or None if not found.
        """
        for flexray in self.flexray_data:
            if flexray.frame_name.replace(".json", ".png") == image_name:
                return flexray
        return None

    def step_next(self) -> Optional[Record]:
        """
        Steps to the next record in the dataset and returns it.

        Returns:
            Optional[Record]: The next record in the dataset, or None if end of dataset is reached.
        """
        try:
            return next(self)
        except StopIteration:
            return None  # When the end of the dataset is reached

    def reset(self):
        """
        Resets the iterator to start from the first record.
        """
        self.index = 0  # Reset index to start over from the first image

    def get_all_data(self) -> list:
        """
        Returns a list of all records (images and their corresponding FlexRay data).

        Returns:
            list[Record]: A list of all records in the dataset.
        """
        records = []
        self.reset()  # Start from the beginning
        while True:
            record = self.step_next()
            if record is None:
                break  # End of dataset
            records.append(record)
        return records

    def get_3d_labels_size(self) -> int:
        """
        Returns the size of the 3D labels data (i.e., the number of image entries).

        Returns:
            int: The number of image records in the 3D labels data.
        """
        return len(self.labels)

    def get_flexray_data_size(self) -> int:
        """
        Returns the size of the FlexRay data (i.e., the number of FlexRay frame entries).

        Returns:
            int: The number of frame records in the FlexRay data.
        """
        return len(self.flexray_data)
