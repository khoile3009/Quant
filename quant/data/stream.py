

from quant.data.config import DatasetConfig
from quant.data.slice import Slice


class DataStream:

    # This method will take in a config and initialize a Datafetcher 
    def __init__(self, config: DatasetConfig):
        pass
    
    # Works like an iterator. Stop when the data reach the end
    def next(self) -> Slice:
        pass