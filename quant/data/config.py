from datetime import datetime
from enum import Enum

from dataclasses import dataclass

class DataSource(Enum):
    BINANCE = "binance"
    
class Interval(Enum):
    M1 = "1m"
    M3 = "3m"
    M5 = "5m"
    M15 = "15m"
    M30 = "30m"
    H1 = "1h"
    H2 = "2h"
    H4 = "4h"
    H6 = "6h"
    H12 = "12h"
    D1 = "1d"
    D3 = "3d"
    W1 = "1w"

class DataType(Enum):
    JSON = "json"
    CSV = "csv"

class Ticker(Enum):
    BTCUSDT = "BTCUSDT"
    ETHUSDT = "ETHUSDT"
    BNBUSDT = "BNBUSDT"

@dataclass
class DataConfig:
    interval: Interval
    ticker: Ticker
    start_time: datetime
    end_time: datetime = None


class DatasetConfig:
    pass