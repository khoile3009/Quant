from abc import ABC, abstractmethod


class Indicator(ABC):
    """
    Indicator statistics
    """

    def __init__(self):
        pass

    @abstractmethod
    def get_required_recall(self):
        """
        Get number of required candle of to calculate the indicator
        """
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def get_value(self, current):
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
