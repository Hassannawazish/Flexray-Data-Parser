# a2d2_dataset/base/base_entry.py

from abc import ABC, abstractmethod
import logging

class BaseEntry(ABC):
    """
    Abstract BaseEntry class defining an interface for data entries.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def load_data(self, file_path: str):
        """
        Abstract method to load data from a given file path.
        """
        pass

    @abstractmethod
    def validate(self):
        """
        Abstract method to validate data.
        """
        pass
