from datetime import datetime
from quant.data.config import BinanceTicker, DataConfig, Interval
from quant.data.data_source import BinanceSource
from quant.utils.time_converter import TimeConverter

if __name__ == "__main__":
    data_config = DataConfig(
        Interval.D1,
        BinanceTicker.BTCUSDT,
        TimeConverter.datetime_to_ms(datetime.strptime("Jun 1 2017", "%b %d %Y")),
    )
    result = BinanceSource.fetch(data_config)
    print(result.head())
