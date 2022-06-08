from datetime import datetime
import os
from dotenv import load_dotenv
import pandas as pd
from quant.data.config import DataConfig, Interval, Ticker


class IO:
    
    @staticmethod
    def get_path_from_config(config: DataConfig) -> str:
        load_dotenv()
        DATA_PATH = os.getenv("DATA_PATH")
        return os.path.join(DATA_PATH, f'{config.ticker.value}_{config.interval.value}.csv') 

    @classmethod
    def save(cls, data: pd.DataFrame, config: DataConfig) -> None:
        path = cls.get_path_from_config(config)
        data.to_csv(path)

    @classmethod
    def load(cls, config: DataConfig) -> pd.DataFrame:
        path = cls.get_path_from_config(config)
        df = pd.read_csv(path, index_col=0)
        df['Open time'], df['Close time'] = pd.to_datetime(
            df['Open time']), pd.to_datetime(df['Close time'])
        df.set_index('Open time', inplace=True)
        return df


if __name__ == "__main__":
    config = DataConfig(Interval.H1, 
                        Ticker.BTCUSDT,
                        datetime.strptime('Jun 1 2018  1:33PM', '%b %d %Y %I:%M%p'),
                        datetime.strptime('Jun 1 2019  1:33PM', '%b %d %Y %I:%M%p')
                        )
    df = IO.load(config)
    print(df.head())