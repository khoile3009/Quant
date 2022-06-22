from datetime import datetime

from regex import R
from quant.data.config import BinanceTicker, DataConfig, Interval, Ticker
from quant.data.data_source import BinanceSource

from quant.utils.io import IO


START_TIME = datetime.strptime("Jun 1 2016  1:33PM", "%b %d %Y %I:%M%p")


if __name__ == "__main__":
    for ticker_name, ticker in BinanceTicker.__members__.items():
        for interval_name, interval in Interval.__members__.items():
            config = DataConfig(interval=interval, ticker=ticker, start_time=START_TIME)
            df = BinanceSource.fetch_server(config)
            IO.save(df, config)
