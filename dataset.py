from typing import Optional
from data_models import ImageData, FlexRayData, Record
from json_parser import load_3d_labels, load_flexray_data

class A2D2Dataset:
    def __init__(self, label_file: str, flexray_file: str):
        """
        Initializes the dataset with paths to 3D label data and FlexRay data files.
        """
        self.labels = load_3d_labels(label_file)
        self.flexray_data = load_flexray_data(flexray_file)

    def match_flexray_data(self, image_name: str) -> Optional[FlexRayData]:
        """
        Matches the FlexRay data with the given image name by comparing frame names.
        """
        for flexray in self.flexray_data:
            if flexray.frame_name.replace(".json", ".png") == image_name:
                return flexray
        return None

    def get_record(self, image_name: str) -> Record:
        """
        Retrieves a complete record containing the 3D label data and the matching FlexRay data.
        If no record is found, returns an empty record with default values.
        """
        # Find the corresponding image data
        image_data = next((img for img in self.labels if img.name == image_name), None)

        # If no image data is found, return an empty record
        if not image_data:
            image_data = ImageData(id="0", name=image_name, width=0, height=0, boxes=[])

        # Find matching FlexRay data, or return an empty placeholder
        flexray_data = self.match_flexray_data(image_name)
        if not flexray_data:
            flexray_data = FlexRayData(frame_name=image_name, timestamp=0, acceleration_x=None, acceleration_y=None)

        # Return the complete record
        return Record(image_data=image_data, flexray_data=flexray_data)

    def get_3d_labels_size(self) -> int:
        """
        Returns the size of the 3D labels data (i.e., the number of image entries).
        """
        return len(self.labels)

    def get_flexray_data_size(self) -> int:
        """
        Returns the size of the FlexRay data (i.e., the number of FlexRay frame entries).
        """
        return len(self.flexray_data)
