import os
from pyspark.sql.functions import col
from pyspark.sql.functions import lit
from pyspark.sql.functions import lower
from pyspark.sql.functions import udf
from data_lake.data_util import DataUtil

#LinkedIn jobs data transform module
class LinkedInJobs(DataUtil):
    def __init__(self, spark_session, source_path):
        super().__init__(spark_session)
        self.source = "Linkedin"
        self.source_path = source_path
    #Generate data for jobs table
    def generate_jobs_table(self, write_path):
        #Replacing column names
        job_cols = ["Job_Title as job_title", "Description as job_description", "Company as company", "Location as location"]
        df_jobs = self.main_df.selectExpr(*job_cols)
        #converting all the job titles to lower case
        df_jobs = df_jobs.withColumn("job_title", lower(df_jobs.job_title))
        #adding column to display source of job
        df_jobs = df_jobs.withColumn("source", lit(self.source))
        w_path = os.path.join(write_path, f"df_jobs_{self.source}.csv")
        df_jobs.toPandas().to_csv(w_path, index=False)
    #Generate data for company_location table                              
    def generate_location_description(self, write_path):
        location_cols = ["Company as company", "Location as location"]
        df_job_location = self.main_df.selectExpr(*location_cols)
        df_job_location = df_job_location.withColumn("city", self._get_city(df_job_location.location))
        df_job_location = df_job_location.withColumn("state", self._get_state(df_job_location.location))
        df_job_location = df_job_location.withColumn("country", self._get_country(df_job_location.location))
        df_job_location = df_job_location.dropDuplicates()
        w_path = os.path.join(write_path, f"df_job_location_{self.source}.csv")
        df_job_location.toPandas().to_csv(w_path, index=False)
