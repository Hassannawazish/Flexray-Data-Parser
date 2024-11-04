# a2d2_dataset/readers/labelled_data_reader.py

import re
from typing import Optional, List
from data_models import ImageData, FlexRayData, Record, DynamicVehicleData
from readers.flexray_data_reader import load_3d_labels, load_flexray_data

class A2D2DatasetIterator:
    """
    Iterator for A2D2 dataset, processing image and FlexRay data frame by frame.
    """

    def __init__(self, label_file: str, flexray_file: str):
        """
        Initializes the dataset with paths to 3D label data and FlexRay data files.
        """
        self.labels = load_3d_labels(label_file)
        self.flexray_data = load_flexray_data(flexray_file)
        self.index = 0  # Start index for iteration over dataset

    def __iter__(self):
        """
        Return the iterator object itself.
        """
        return self

    def __next__(self) -> Record:
        """
        Returns the next Record in the dataset, combining 3D label data and FlexRay data.

        Returns:
            Record: The next combined data record.
        """
        if self.index >= len(self.labels):
            raise StopIteration

        image_data = self.labels[self.index]
        flexray_data = self.find_closest_flexray_data(self.flexray_data[self.index].timestamp)
        self.index += 1
        return Record(image_data=image_data, flexray_data=flexray_data)

    def find_closest_flexray_data(self, frame_timestamp: int) -> Optional[FlexRayData]:
        """
        Finds the closest FlexRay data to the given frame timestamp.

        Args:
            frame_timestamp (int): The timestamp of the frame.

        Returns:
            Optional[FlexRayData]: The closest FlexRayData object.
        """
        closest_flexray = None
        min_time_diff = float('inf')

        for flexray in self.flexray_data:
            time_diff = abs(flexray.timestamp - frame_timestamp)
            if time_diff < min_time_diff:
                min_time_diff = time_diff
                closest_flexray = FlexRayData(
                    frame_name=flexray.frame_name,
                    timestamp=flexray.timestamp,
                    **{param: self.find_closest_dynamic_data(getattr(flexray, param), frame_timestamp)
                       for param in flexray.__annotations__.keys() if param not in ('frame_name', 'timestamp')}
                )

        return closest_flexray

    @staticmethod
    def find_closest_dynamic_data(dynamic_data: DynamicVehicleData, target_timestamp: int) -> DynamicVehicleData:
        """
        Finds the closest data point within DynamicVehicleData to the target timestamp.

        Args:
            dynamic_data (DynamicVehicleData): The data set to search.
            target_timestamp (int): The target timestamp.

        Returns:
            DynamicVehicleData: The closest DynamicVehicleData point.
        """
        min_time_diff = float('inf')
        closest_timestamp = None
        closest_value = None

        for ts, value in zip(dynamic_data.timestamps, dynamic_data.values):
            time_diff = abs(ts - target_timestamp)
            if time_diff < min_time_diff:
                min_time_diff = time_diff
                closest_timestamp = ts
                closest_value = value

        return DynamicVehicleData(
            timestamps=[closest_timestamp],
            values=[closest_value],
            unit=dynamic_data.unit
        )

    def step_next(self) -> Optional[Record]:
        """
        Retrieves the next record in the dataset, or returns None if at the end.

        Returns:
            Optional[Record]: The next record or None if finished.
        """
        try:
            return next(self)
        except StopIteration:
            return None

    def reset(self):
        """
        Resets the iterator to the first frame.
        """
        self.index = 0

    def get_all_data(self) -> List[Record]:
        """
        Retrieves all data records in the dataset.

        Returns:
            list: A list of all records in the dataset.
        """
        records = []
        self.reset()
        while True:
            record = self.step_next()
            if record is None:
                break
            records.append(record)
        return records

    def get_3d_labels_size(self) -> int:
        """
        Returns the number of 3D label entries in the dataset.

        Returns:
            int: The number of 3D label entries.
        """
        return len(self.labels)

    def get_flexray_data_size(self) -> int:
        """
        Returns the size of the FlexRay data (i.e., the number of FlexRay frame entries).

        Returns:
            int: The number of frame records in the FlexRay data.
        """
        return len(self.flexray_data)
