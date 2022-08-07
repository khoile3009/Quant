"""
Data configuration
"""
from ctypes import ArgumentError
from datetime import datetime
from enum import Enum

from dataclasses import dataclass
import math
from typing import Dict, List, Optional

from quant.data.indicators import Indicator

SECONDS_PER_UNIT = {"m": 60, "h": 60 * 60, "d": 24 * 60 * 60, "w": 7 * 24 * 60 * 60}


class Interval(Enum):
    """
    Interval for a ticker
    """

    M1 = "1m"
    M3 = "3m"
    M5 = "5m"
    M15 = "15m"
    M30 = "30m"
    H1 = "1h"
    H2 = "2h"
    H4 = "4h"
    H6 = "6h"
    H12 = "12h"
    D1 = "1d"
    D3 = "3d"
    W1 = "1w"

    @property
    def seconds(self):
        """
        Get seconds of an interval
        """
        time_value = int(self.value[:-1])
        unit = self.value[-1]
        unit_second = SECONDS_PER_UNIT.get(unit)
        return unit_second * time_value

    # TODO: This might be used a lot, which lead to waste of computation. Think about how to cache it or turn it into constant since its not changing
    @property
    def milis(self):
        """
        Get ms of an interval
        """
        return self.seconds * 1000

    @staticmethod
    def from_seconds(second: int) -> "Interval":
        """
        Get interval from seconds
        """
        smallest_unit = None
        for unit, unit_second in SECONDS_PER_UNIT.items():
            if second >= unit_second and second % unit_second == 0:
                smallest_unit = unit
            else:
                break
        return Interval[
            f'{smallest_unit.capitalize()}{second // SECONDS_PER_UNIT.get(smallest_unit, "0")}'
        ]

    def gcd(self, other: "Interval") -> "Interval":
        """
        GCD of 2 interval
        """
        if not other:
            return self

        if self.divisible(other):
            raise ArgumentError("Argument is not divisible by this object")

        gcd_second = math.gcd(self.seconds, other.seconds)
        return Interval.from_seconds(gcd_second)

    @classmethod
    def list_gcd(cls, intervals: List["Interval"]) -> "Interval":
        """
        GCD of intervals
        """
        if len(intervals) == 0:
            return None

        greatest_common_interval = None
        for interval in intervals:
            greatest_common_interval = interval.gcd(greatest_common_interval)

        return greatest_common_interval

    def divisible(self, interval: "Interval") -> bool:
        """
        Return if object is divisible by an interval
        """
        return self.seconds % interval.seconds

    def difference(self, interval: "Interval") -> int:
        """
        Difference of 2 interval
        """
        if self.divisible(interval):
            raise ArgumentError("Argument is not divisible by this object")

        return self.seconds // interval.seconds


class Ticker(Enum):
    """
    Ticker abstract enum
    """


class BinanceTicker(Ticker):
    """
    Binance's ticker
    """

    BTCUSDT = "BTCUSDT"
    ETHUSDT = "ETHUSDT"
    BNBUSDT = "BNBUSDT"


@dataclass
class DataConfig:
    """
    Data configuration
    """

    interval: Interval
    ticker: Ticker
    start_time: int
    end_time: int = None

    def __hash__(self) -> int:
        return hash(self.ticker.value + self.interval.value)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, DataConfig):
            return False

        return (self.ticker.value + self.interval.value) == (
            __o.ticker.value + __o.interval.value
        )


@dataclass
class DatasetConfig:
    """
    Data configuration for datastream
    """

    intervals: List[Interval]
    tickers: List[Ticker]
    start_time: int
    end_time: int
    indicators: List[Indicator]
    required_recall: Optional[int] = 0

    def __post_init__(self):
        self.common_interval = Interval.list_gcd(self.intervals)

    def get_minimal_dataconfigs(self):
        """
        Return the minimal dataconfigs
        """
        return [
            DataConfig(
                interval=self.common_interval,
                ticker=ticker,
                start_time=self.start_time,
                end_time=self.end_time,
            )
            for ticker in self.tickers
        ]

    def get_dataconfigs(self) -> Dict[DataConfig, DataConfig]:
        """
        Get data configs and map to the gcd of list
        """
        dataconfigs_map = {}
        for ticker in self.tickers:
            common_config = DataConfig(
                interval=self.common_interval,
                ticker=ticker,
                start_time=self.start_time,
                end_time=self.end_time,
            )
            for interval in self.intervals:
                dataconfigs_map[
                    DataConfig(
                        interval=interval,
                        ticker=ticker,
                        start_time=self.start_time,
                        end_time=self.end_time,
                    )
                ] = common_config

        return dataconfigs_map


if __name__ == "__main__":
    a = Interval.from_seconds(300)
    b = Interval.M15
    c = Interval.H1
    print(Interval.list_gcd([a, b, c]))
