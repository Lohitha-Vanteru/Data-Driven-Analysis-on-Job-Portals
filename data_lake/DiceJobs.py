# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

"""Dice Data Transformer Module"""

import os

from pyspark.sql.functions import col,length
from pyspark.sql.functions import lit
from pyspark.sql.functions import lower
from pyspark.sql.functions import udf

from data_lake.data_util import DataUtil


class DiceJobs(DataUtil):
    """Dice Data Transformer"""

    def __init__(self, spark_session, source_path):
        super().__init__(spark_session)

        self.source = "Dice"
        self.source_path = source_path

    def generate_jobs_table(self, write_path):
        """Generate data for jobs table"""
        df_jobs = self.main_df.select(col("job_title").alias("job_title"),
                                      col("job_description").alias("job_description"),
                                      col("organization").alias("company"),
                                      col("location").alias("location"))

        df_jobs = df_jobs.withColumn("job_title", lower(df_jobs.job_title))
        df_jobs = df_jobs.withColumn("source", lit(self.source))
        df_jobs=df_jobs.filter(length(col("job_description"))<255)

        w_path = os.path.join(write_path, f"df_jobs_{self.source}.csv")
        df_jobs.toPandas().to_csv(w_path, index=False)

    def generate_location_description(self, write_path):
        """Generate data for company_location table"""
        df_job_location = self.main_df.select(col("organization").alias("company"),col("location").alias("location"))
        df_job_location = df_job_location.dropna()
        df_job_location = df_job_location.withColumn("city", self._get_city(df_job_location.location))
        df_job_location = df_job_location.withColumn("state", self._get_state(df_job_location.location))
        df_job_location = df_job_location.withColumn("country", self._get_country(df_job_location.location))
        df_job_location = df_job_location.dropDuplicates()

        w_path = os.path.join(write_path, f"df_job_location_{self.source}.csv")
        df_job_location.toPandas().to_csv(w_path, index=False)

    def generate_job_sector(self, write_path):
        """Generate data for job_sector table"""
        df_job_sector = self.main_df.select(col("job_title").alias("job_title"),
                                            col("sector").alias("sector"))

        df_job_sector = df_job_sector.dropDuplicates()

        w_path = os.path.join(write_path, f"df_job_sectors_{self.source}.csv")
        df_job_sector.toPandas().to_csv(w_path, index=False)
