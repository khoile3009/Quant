from abc import ABC, abstractmethod
from dataclasses import dataclass
from re import L
from typing import Set, Tuple

from quant.trade.asset import Asset


@dataclass
class ActionResult:
    """
    Action result
    """

    account: float
    to_add: Set[Asset]
    to_remove: Set[Asset]


class Action(ABC):
    """
    Abstract class for action
    """

    @abstractmethod
    def get_result(self) -> ActionResult:
        """
        Apply the action to portfolio
        """
