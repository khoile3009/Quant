from datetime import datetime
from abc import ABC, abstractmethod
from os import getenv
from typing import List, Union

from binance.client import Client
import pandas as pd
import numpy as np
from dotenv import load_dotenv

from quant.data.config import BinanceTicker, DataConfig, Interval
from quant.utils.io import IO
from quant.utils.time_converter import TimeConverter


class DataSource(ABC):
    """
    Source of candle data
    """

    # 1 datastream connect to many data source.
    @staticmethod
    def fetch(config: DataConfig) -> pd.DataFrame:
        """
        Fetch data
        """


def get_binance_client():
    """
    Get a binance client
    """
    load_dotenv()
    binance_api = getenv("BINANCE_API_KEY")
    binance_secret = getenv("BINANCE_SECRET_KEY")
    return Client(binance_api, binance_secret)


class BinanceSource(DataSource):
    """
    Binance data source
    """

    COLUMN_NAMES = [
        "Open time",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "Close time",
        "Quote asset volume",
        "Number of trades",
        "Taker buy base asset volume",
        "Taker buy quote asset volume",
    ]

    MAX_BINANCE_LIMIT = 1000

    @staticmethod
    def convert_rest_output(rest_output: List[str]) -> List[Union[int, float]]:
        """
        Convert to rest output
        """
        for index, string_list in enumerate(rest_output):
            rest_output[index] = (
                [int(string_list[0])]
                + [float(x) for x in string_list[1:6]]
                + [int(string_list[6])]
                + [float(x) for x in string_list[7:-1]]
            )
        return rest_output

    @classmethod
    def convert_to_dataframe(cls, kline_list: List[Union[int, float]]) -> pd.DataFrame:
        """
        Convert kline array to dataframe
        """
        dataframe = pd.DataFrame(kline_list, columns=cls.COLUMN_NAMES)
        return dataframe

    @staticmethod
    def fetch_server(config: DataConfig) -> pd.DataFrame:
        """
        This method fetch from  server
        """
        if not config:
            return None

        client = get_binance_client()

        # Because binance only allow to fetch 1000 at a time, therefore we fetch 1000 each time and append it
        output_data = []
        kline_data = BinanceSource.convert_rest_output(
            client.get_klines(
                symbol=config.ticker.value,
                interval=config.interval.value,
                startTime=config.start_time,
                endTime=config.end_time,
                limit=BinanceSource.MAX_BINANCE_LIMIT,
            )
        )
        output_data += kline_data
        while len(kline_data) > 0 and (
            not config.end_time or kline_data[-1][0] < config.end_time
        ):
            new_start_time = kline_data[-1][0] + TimeConverter.interval_to_ms(
                config.interval
            )
            kline_data = BinanceSource.convert_rest_output(
                client.get_klines(
                    symbol=config.ticker.value,
                    interval=config.interval.value,
                    startTime=new_start_time,
                    endTime=config.end_time,
                    limit=BinanceSource.MAX_BINANCE_LIMIT,
                )
            )
            output_data += kline_data

        # TODO: Trim the end if the endtime is specified
        # print([r[0] for r in output_data[:10]])
        # Convert to csv
        output_csv = BinanceSource.convert_to_dataframe(output_data)
        return output_csv

    @staticmethod
    def fetch(config: DataConfig) -> pd.DataFrame:
        dataframe = IO.load(config)
        if config.end_time:
            dataframe = dataframe.loc[
                (dataframe["Open time"] >= config.start_time)
                & (dataframe["Close time"] <= config.end_time)
            ]
        else:
            dataframe = dataframe.loc[dataframe["Open time"] >= config.start_time]
        return dataframe


# Rerouter for datasource
class MasterDataSource(DataSource):
    """
    Master data source to route
    """

    @staticmethod
    def fetch(config: DataConfig) -> pd.DataFrame:
        if isinstance(config.ticker, BinanceTicker):
            return BinanceSource.fetch(config)


if __name__ == "__main__":
    data_config = DataConfig(
        Interval.D1,
        BinanceTicker.BTCUSDT,
        TimeConverter.datetime_to_ms(datetime.strptime("Jun 1 2018", "%b %d %Y")),
        TimeConverter.datetime_to_ms(datetime.strptime("Jun 1 2019", "%b %d %Y")),
    )
    result = BinanceSource.fetch_server(data_config)
    # print(result.head(10)["Open time"].to_list())
