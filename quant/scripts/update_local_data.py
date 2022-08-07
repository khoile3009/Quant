"""
Script to update all local data
"""
from datetime import datetime

from quant.data.config import BinanceTicker, DataConfig, Interval, Ticker
from quant.data.data_source import BinanceSource

from quant.utils.io import IO
from quant.utils.time_converter import TimeConverter


START_TIME = TimeConverter.datetime_to_ms(
    datetime.strptime("Jun 1 2016  1:33PM", "%b %d %Y %I:%M%p")
)


if __name__ == "__main__":
    for ticker_name, ticker in BinanceTicker.__members__.items():
        for interval_name, interval in Interval.__members__.items():
            config = DataConfig(interval=interval, ticker=ticker, start_time=START_TIME)
            df = BinanceSource.fetch_server(config)
            IO.save(df, config)
