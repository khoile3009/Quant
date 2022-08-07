from dataclasses import dataclass
from typing import Set
from quant.trade.action import Action

from quant.trade.asset import Asset


@dataclass
class Portfolio:
    """
    Portfolio of an account
    """

    account: float
    assets: Set[Asset]

    def apply(self, action: Action):
        """
        Apply action to account
        """
        action_result = action.get_result()
        # TODO: Check to see if we have enough account or
        self.account += action_result.account
        for asset in action_result.to_remove:
            self.assets.remove(asset)
        for asset in action_result.to_add:
            self.assets.add(asset)

    def get_total_value(self) -> float:
        return self.account + sum([asset.value for asset in self.assets])
