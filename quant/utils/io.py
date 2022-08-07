"""
This module is for IO stuffs
"""

from datetime import datetime
import os
from dotenv import load_dotenv
import pandas as pd
from quant.data.config import BinanceTicker, DataConfig, Interval


class IO:
    """
    IO stream
    """

    @staticmethod
    def get_path_from_config(config: DataConfig) -> str:
        """
        Get path from config
        """
        load_dotenv()
        data_path = os.getenv("DATA_PATH")
        return os.path.join(
            data_path, f"{config.ticker.value}_{config.interval.value}.csv"
        )

    @classmethod
    def save(cls, data: pd.DataFrame, config: DataConfig) -> None:
        """
        Save dataframe to storage
        """
        path = cls.get_path_from_config(config)
        data.to_csv(path)

    @classmethod
    def load(cls, config: DataConfig) -> pd.DataFrame:
        """
        Load dataframe from storage
        """
        path = cls.get_path_from_config(config)
        dataframe = pd.read_csv(path, index_col=0)
        return dataframe


if __name__ == "__main__":
    data_config = DataConfig(
        Interval.H1,
        BinanceTicker.BTCUSDT,
        datetime.strptime("Jun 1 2018  1:33PM", "%b %d %Y %I:%M%p"),
        datetime.strptime("Jun 1 2019  1:33PM", "%b %d %Y %I:%M%p"),
    )
    print(IO.load(data_config).head())
