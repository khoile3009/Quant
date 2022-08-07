"""
Data stream
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional


from quant.data.config import BinanceTicker, DataConfig, DatasetConfig, Interval
from quant.data.data_row import DataRow
from quant.data.data_source import MasterDataSource
from quant.data.indicators import Indicator
from quant.utils.time_converter import TimeConverter


@dataclass
class DataWithIndicator:
    """
    Data row combined with indicators
    """

    data_row: DataRow
    indicators: Dict[Indicator, float]

    @classmethod
    def from_recall_and_indicators(
        cls, current_row: DataRow, recall: List[DataRow], indicators: List[Indicator]
    ) -> "DataWithIndicator":
        """
        Create an object from recall and indicators
        """
        indicator_values = {
            indicator: indicator.get_value(recall) for indicator in indicators
        }
        return DataWithIndicator(data_row=current_row, indicators=indicator_values)


class DataAccumulator:
    """
    Accumulating data for Binance
    """

    def __init__(self, interval: Interval, indicators: List[Indicator]):
        self.interval_ms = interval.milis
        self.indicators = indicators
        self.cummulated_row: Optional[DataRow] = None
        self.num_required_recall = Indicator.get_max_required_recall(self.indicators)
        self.recall = []
        self.current_data_with_indicator: Optional[DataWithIndicator] = None
        self.original_time = None

    def add_row(self, row: DataRow) -> DataWithIndicator:
        """
        Add new row to the accumulator
        """

        def add_to_recall(row_to_add: DataRow):
            self.recall.append(row_to_add)
            if len(self.recall) == self.num_required_recall:
                self.recall.pop(0)

        def is_different_interval():
            current_open_div = (row.open_time - self.original_time) // self.interval_ms
            last_open_div = (
                self.cummulated_row.open_time - self.original_time
            ) // self.interval_ms

            return current_open_div > last_open_div

        if not self.cummulated_row:
            print("start")
            self.cummulated_row = row
            self.original_time = row.open_time

        elif is_different_interval():
            print("cummulated")
            add_to_recall(self.cummulated_row)
            self.cummulated_row = row
        else:
            print("not")
            self.cummulated_row = self.cummulated_row.add_row(row)

        self.current_data_with_indicator = DataWithIndicator.from_recall_and_indicators(
            self.cummulated_row, self.recall, self.indicators
        )
        print(self.cummulated_row)
        return self.current_data_with_indicator

    def current_data(self) -> DataRow:
        """
        Get current data row
        """
        return self.current_data_with_indicator


@dataclass
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


class DataStream(ABC):
    """
    Datastream that stream data for bactest
    """

    @abstractmethod
    def next(self) -> DataSlice:
        """
        Next dataslice
        """
        pass


class DatasetStream:
    """
    Datastream that stream data from offline dataset
    """

    def __init__(self, dataset_config: DatasetConfig):
        self.dataconfigs = dataset_config.get_dataconfigs()
        minimal_dataconfigs = dataset_config.get_minimal_dataconfigs()
        self.datasets = {
            minimal_dataconfig: MasterDataSource.fetch(minimal_dataconfig)
            for minimal_dataconfig in minimal_dataconfigs
        }
        self.data_accumulators = {
            data_config: DataAccumulator(
                interval=data_config.interval, indicators=dataset_config.indicators
            )
            for data_config in self.dataconfigs
        }
        self.current_row = 0

    # Works like an iterator. Stop when the data reach the end
    def next(self) -> DataSlice:
        """
        Next dataslice from the dataset
        """
        data = {}
        for data_config, data_accumulator in self.data_accumulators.items():
            minimal_dataconfig = self.dataconfigs.get(data_config)
            minimal_dataset = self.datasets.get(minimal_dataconfig)
            df_row = minimal_dataset.iloc[self.current_row]
            data_row = DataRow.from_df_row(df_row)
            self.data_accumulators[data_config].add_row(data_row)
        self.current_row += 1


if __name__ == "__main__":
    datasetconfig = DatasetConfig(
        intervals=[Interval.D1, Interval.D3],
        tickers=[BinanceTicker.BNBUSDT],
        start_time=TimeConverter.datetime_to_ms(
            datetime.strptime("Jun 1 2018", "%b %d %Y")
        ),
        end_time=TimeConverter.datetime_to_ms(
            datetime.strptime("Jun 1 2019", "%b %d %Y")
        ),
        indicators=[],
    )
    datastream = DatasetStream(dataset_config=datasetconfig)
    datastream.next()
    datastream.next()
    datastream.next()
    datastream.next()
    datastream.next()
    datastream.next()
