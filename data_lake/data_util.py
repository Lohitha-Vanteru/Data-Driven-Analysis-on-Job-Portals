from pyspark.sql.functions import udf

# Base utitly class with common functions to inherit
class DataUtil:
    def __init__(self, spark_session):
        self.spark = spark_session
        self.main_df = None
    
    #Read data from the source path and assign it to main df attribute
    def read_data_from_source(self):
        self.main_df = self.spark.read.csv(self.source_path,header=True, sep=",", multiLine=True, escape='"')

    #Read data from the source path and assign it to main df attribute
    def read_data_from_source_parquet(self):
        self.main_df = self.spark.read.parquet(self.source_path,header=True)

    #Free data from memory
    def unload_dataframe(self):
        try:
            del self.main_df
        except KeyError:
            pass
        finally:
            self.main_df = None

    #Get city from the string of specific pattern: city, state, country
    @staticmethod
    @udf
    def _get_city(x):
        if len(x.split(",")) >= 1:
            return x.split(",")[0]
        return None

    #Get state from the string of specific pattern: city, state, country
    @staticmethod
    @udf
    def _get_state(x):
        if len(x.split(",")) >= 2:
            return x.split(",")[1]
        return None

    #Get country from the string of specific pattern: city, state, country
    @staticmethod
    @udf
    def _get_country(x):
        if len(x.split(",")) >= 3:
            return x.split(",")[2]
        return None
