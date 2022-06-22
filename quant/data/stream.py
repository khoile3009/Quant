from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

from quant.data.config import BinanceTicker, DataConfig, DatasetConfig, Interval
from quant.data.data_source import DataSource, MasterDataSource
from quant.data.indicators import Indicator


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
    quote_asset_volume: float = None
    number_of_trades: int = None
    taker_buy_base_asset_volumn: int = None
    taker_buy_quote_asset_volumn: int = None


@dataclass
class DataWithIndicator:
    """
    Data row combined with indicators
    """

    data_row: DataRow
    indicators: Dict[Indicator, float]


class DataSlice:
    """
    Data slice to be returned each time
    """

    data: Dict[DataConfig, List[DataWithIndicator]]

    def get(self, data_config: DataConfig) -> List[DataWithIndicator]:
        """
        Getter method for dataconfig
        """
        return self.data.get(data_config)


class DataStream:
    """
    Data stream that stream data for bactest
    """

    def __init__(self, dataset_config: DatasetConfig):
        self.dataconfigs = dataset_config.get_dataconfigs()
        minimal_dataconfigs = dataset_config.get_minimal_dataconfigs()
        self.datasets = {
            minimal_dataconfig: MasterDataSource.fetch(minimal_dataconfig)
            for minimal_dataconfig in minimal_dataconfigs
        }

    # Works like an iterator. Stop when the data reach the end
    def next(self) -> DataSlice:
        """
        Next dataslice from the dataset
        """
        pass


if __name__ == "__main__":
    datasetconfig = DatasetConfig(
        intervals=[Interval.D1, Interval.D3],
        tickers=[BinanceTicker.BNBUSDT, BinanceTicker.BTCUSDT],
        start_time=datetime.strptime("Jun 1 2018", "%b %d %Y"),
        end_time=datetime.strptime("Jun 1 2019", "%b %d %Y"),
        indicators=[],
    )
    datastream = DataStream(dataset_config=datasetconfig)
    for k, v in datastream.dataconfigs.items():
        print(k, v)
