"""
Abtract class for indicator
"""

from abc import ABC, abstractmethod
from typing import List

from quant.data.data_row import DataRow


class Indicator(ABC):
    """
    Indicator statistics
    """

    def __init__(self):
        pass

    @abstractmethod
    def get_required_recall(self) -> int:
        """
        Get number of required candle of to calculate the indicator
        """
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def get_value(self, recall: List[DataRow]):
        """
        Get value of the indicator
        """
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def __hash__(self) -> int:
        """
        Hash function of object
        """
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def __eq__(self, __o: object) -> bool:
        """
        Comparing if two object is equal
        """
        raise NotImplementedError("Not implemented")

    @classmethod
    def get_max_required_recall(cls, indicators: List["Indicator"]) -> int:
        """
        Get max required recall for a list of indicator
        """
        if len(indicators) == 0:
            return 0
        return max([indicator.get_required_recall() for indicator in indicators])
