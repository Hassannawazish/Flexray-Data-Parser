# a2d2_dataset/dataset.py

import re
from typing import Optional
from data_models import ImageData, FlexRayData, Record, AccelerationData
from json_parser import load_3d_labels, load_flexray_data

class A2D2DatasetIterator:
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
        Moves to the next image record in the dataset by timestamp.
        Raises StopIteration when the end of the dataset is reached.
        """
        if self.index >= len(self.labels):
            raise StopIteration

        image_data = self.labels[self.index]
        flexray_data = self.find_closest_flexray_data(self.flexray_data[self.index].timestamp)

        self.index += 1
        return Record(image_data=image_data, flexray_data=flexray_data)

    def find_closest_flexray_data(self, frame_timestamp: int) -> Optional[FlexRayData]:
        """
        Finds the FlexRay data entry with the closest timestamp to the given frame timestamp
        and returns only the data for that closest timestamp.

        Args:
            frame_timestamp (int): The timestamp from the FlexRay entry.

        Returns:
            Optional[FlexRayData]: The FlexRay data entry closest to the frame timestamp, with only the
            acceleration data for the closest timestamp.
        """
        closest_flexray = None
        min_time_diff = float('inf')

        # Iterate through FlexRay data entries to find the one with the closest timestamp
        for flexray in self.flexray_data:
            time_diff = abs(flexray.timestamp - frame_timestamp)

            if time_diff < min_time_diff:
                min_time_diff = time_diff
                # Find the closest individual timestamp within the acceleration data timestamps
                closest_accel_x = self.find_closest_accel_data(flexray.acceleration_x, frame_timestamp)
                closest_accel_y = self.find_closest_accel_data(flexray.acceleration_y, frame_timestamp)

                # Create a FlexRayData object with only the closest timestamp data
                closest_flexray = FlexRayData(
                    frame_name=flexray.frame_name,
                    timestamp=flexray.timestamp,
                    acceleration_x=closest_accel_x,
                    acceleration_y=closest_accel_y
                )

        return closest_flexray

    @staticmethod
    def find_closest_accel_data(accel_data: AccelerationData, target_timestamp: int) -> AccelerationData:
        """
        Finds the closest timestamp in acceleration data and returns only that timestamp and value.

        Args:
            accel_data (AccelerationData): The acceleration data containing timestamps and values.
            target_timestamp (int): The target timestamp to match.

        Returns:
            AccelerationData: A new AccelerationData object with only the closest timestamp and its value.
        """
        min_time_diff = float('inf')
        closest_timestamp = None
        closest_value = None

        for ts, value in zip(accel_data.timestamps, accel_data.values):
            time_diff = abs(ts - target_timestamp)
            if time_diff < min_time_diff:
                min_time_diff = time_diff
                closest_timestamp = ts
                closest_value = value

        return AccelerationData(
            timestamps=[closest_timestamp],
            values=[closest_value],
            unit=accel_data.unit
        )

    def step_next(self) -> Optional[Record]:
        try:
            return next(self)
        except StopIteration:
            return None

    def reset(self):
        self.index = 0

    def get_all_data(self) -> list:
        records = []
        self.reset()
        while True:
            record = self.step_next()
            if record is None:
                break
            records.append(record)
        return records

    def get_3d_labels_size(self) -> int:
        return len(self.labels)

    def get_flexray_data_size(self) -> int:
        """
        Returns the size of the FlexRay data (i.e., the number of FlexRay frame entries).

        Returns:
            int: The number of frame records in the FlexRay data.
        """
        return len(self.flexray_data)
