"""
Data row representation
"""

from datetime import datetime
from attr import dataclass

import pandas as pd


@dataclass
class DataRow:
    """
    An object to reflect a row in dataframe
    """

    open_time: datetime
    open: float
    close: float
    high: float
    low: float
    volume: float
    close_time: datetime

    def __str__(self) -> str:
        return f"{self.open_time} {self.open} {self.close} {self.high} {self.low} {self.volume} {self.close_time}"

    def add_row(self, row: "DataRow") -> "DataRow":
        """
        Add a datarow
        """
        new_row = DataRow(
            open_time=self.open_time,
            open=self.open,
            close=row.close,
            high=max(self.high, row.high),
            low=min(self.low, row.low),
            volume=self.volume + row.volume,
            close_time=row.close_time,
        )
        return new_row

    @staticmethod
    def from_df_row(df_row: pd.Series) -> "DataRow":
        """
        Create a data row from df row
        """
        return DataRow(
            open_time=df_row["Open time"],
            open=df_row["Open"],
            close=df_row["Close"],
            high=df_row["High"],
            low=df_row["Low"],
            volume=df_row["Volume"],
            close_time=df_row["Close time"],
        )
