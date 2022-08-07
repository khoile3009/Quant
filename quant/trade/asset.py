from abc import ABC


class Asset(ABC):
    """
    Abstract class for asset
    """

    @property
    def value(self) -> float:
        """
        Current value of the asset
        """
