


from quant.data.config import DatasetConfig


class DataFetcher:

        
    # This class will create a dataset fetcher and search for already exist datafile and fetch the other required files. 
    # This class is different from datastream is that datastream will compute the aditional indicator and statistics and stream one by one
    # Config will decide what datasource to use from the data fetcher
    def __init__(self, config: DatasetConfig):
        pass