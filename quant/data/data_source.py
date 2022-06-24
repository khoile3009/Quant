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
    @abstractmethod
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
        for string_list, index in enumerate(rest_output):
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
        kline_array = np.array(kline_list, dtype=np.float32)
        df = pd.DataFrame(kline_array, columns=cls.COLUMN_NAMES)
        df["Open time"] = df["Open time"].apply(TimeConverter.ms_to_datetime)
        df["Close time"] = df["Close time"].apply(TimeConverter.ms_to_datetime)
        return df

    @staticmethod
    def fetch_server(config: DataConfig) -> pd.DataFrame:
        """
        This method fetch from  server
        """
        if not config:
            return None

        client = get_binance_client()

        start_ms = TimeConverter.datetime_to_ms(config.start_time)
        end_ms = TimeConverter.datetime_to_ms(config.end_time)

        # Because binance only allow to fetch 1000 at a time, therefore we fetch 1000 each time and append it
        output_data = []
        kline_data = BinanceSource.convert_rest_output(
            client.get_klines(
                symbol=config.ticker.value,
                interval=config.interval.value,
                startTime=start_ms,
                endTime=end_ms,
                limit=BinanceSource.MAX_BINANCE_LIMIT,
            )
        )
        output_data += kline_data
        while len(kline_data) > 0 and (not end_ms or kline_data[-1][0] < end_ms):
            new_start_ms = kline_data[-1][0] + TimeConverter.interval_to_ms(
                config.interval
            )
            kline_data = BinanceSource.convert_rest_output(
                client.get_klines(
                    symbol=config.ticker.value,
                    interval=config.interval.value,
                    startTime=new_start_ms,
                    endTime=end_ms,
                    limit=BinanceSource.MAX_BINANCE_LIMIT,
                )
            )
            output_data += kline_data

        # TODO: Trim the end if the endtime is specified

        # Convert to csv
        output_csv = BinanceSource.convert_to_dataframe(output_data)
        return output_csv

    @staticmethod
    def fetch(config: DataConfig) -> pd.DataFrame:
        dataframe = IO.load(config)
        dataframe = dataframe.loc[
            (dataframe.index >= np.datetime64(config.start_time))
            & (dataframe.index <= np.datetime64(config.end_time))
        ]
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
        datetime.strptime("Jun 1 2018", "%b %d %Y"),
        datetime.strptime("Jun 1 2019", "%b %d %Y"),
    )
    result = BinanceSource.fetch(data_config)
    print(result.head())
