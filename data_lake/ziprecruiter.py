import os

from pyspark.sql.functions import col,length
from pyspark.sql.functions import lit
from pyspark.sql.functions import lower
from pyspark.sql.functions import udf
from data_lake.data_util import DataUtil

#Ziprecruiter jobs data transform module
class ZiprecruiterJobs(DataUtil):
    def __init__(self, spark_session, source_path):
        super().__init__(spark_session)
        self.source = "Zip recruiter"
        self.source_path = source_path
    #Generate data for jobs table
    def generate_jobs_table(self, write_path):
        df_jobs = self.main_df.select(col("job_title").alias("job_title"), col("job_description").alias("job_description"), col("company_name").alias("company"), col("city").alias("location"))
        #converting all the job titles to lower case
        df_jobs = df_jobs.withColumn("job_title", lower(df_jobs.job_title))
        df_jobs=df_jobs.filter(length(col("company"))<255)
        #adding column to display source of job
        df_jobs = df_jobs.withColumn("source", lit(self.source))
        w_path = os.path.join(write_path, f"df_jobs_{self.source}.csv")
        df_jobs.toPandas().to_csv(w_path, index=False)
    #Generate data for company_location table
    def generate_location_description(self, write_path):
        df_job_location = self.main_df.select(col("company_name").alias("company"),col("city").alias("location"),col("city").alias("city"),col("state").alias("state"))
        df_job_location =df_job_location.filter(length(col("company"))<255)
        df_job_location = df_job_location.withColumn("city", df_job_location.city)
        df_job_location = df_job_location.withColumn("state",df_job_location.state)
        df_job_location = df_job_location.withColumn("country", lit("US"))
        df_job_location = df_job_location.dropDuplicates()
        w_path = os.path.join(write_path, f"df_job_location_{self.source}.csv")
        df_job_location.toPandas().to_csv(w_path, index=False)
    #Generate data for job_sector table
    def generate_job_sector(self, write_path):
        df_job_sector = self.main_df.select(col("job_title").alias("job_title"), col("category").alias("sector"))
        df_job_sector = df_job_sector.dropDuplicates()
        w_path = os.path.join(write_path, f"df_job_sectors_{self.source}.csv")
        df_job_sector.toPandas().to_csv(w_path, index=False)
