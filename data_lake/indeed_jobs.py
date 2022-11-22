import os
from pyspark.sql.functions import col
from pyspark.sql.functions import lit
from pyspark.sql.functions import lower
from pyspark.sql.functions import udf
from data_lake.data_util import DataUtil

#Indeed jobs data transform module
class IndeedJobs(DataUtil):
    def __init__(self, spark_session, source_path):
        super().__init__(spark_session)
        self.source = "Indeed"
        self.source_path = source_path
    #Generate data for jobs table
    def generate_jobs_table(self, write_path):
        #Replacing column names
        job_cols = ["title as job_title", "description as job_description", "company as company", "city as location"]
        df_jobs = self.main_df.selectExpr(*job_cols)
        #converting all the job titles to lower case
        df_jobs = df_jobs.withColumn("job_title", lower(df_jobs.job_title))
        #adding column to display source of job
        df_jobs = df_jobs.withColumn("source", lit(self.source))
        w_path = os.path.join(write_path, f"df_jobs_{self.source}.csv")
        df_jobs.toPandas().to_csv(w_path, index=False)
    #Generate data for company_location table
    def generate_location_description(self, write_path):
        #Replacing column names
        location_cols = ["company as company", "city as location","city as city","state as state"]
        df_job_location = self.main_df.selectExpr(*location_cols)
        df_job_location = df_job_location.withColumn("city", df_job_location.city)
        df_job_location = df_job_location.withColumn("state",df_job_location.state)
        df_job_location = df_job_location.withColumn("country", lit("US"))
        df_job_location = df_job_location.dropDuplicates()
        w_path = os.path.join(write_path, f"df_job_location_{self.source}.csv")
        df_job_location.toPandas().to_csv(w_path, index=False)
    #Generate data for job_rating table
    def generate_job_reviews(self, write_path):
        #Replacing column names
        review_cols = ["title as job_title", "company as company", "rating as rating"]
        df_job_reviews = self.main_df.selectExpr(*review_cols)
        #adding column for maximum rating i.e, 5 in this case
        df_job_reviews = df_job_reviews.withColumn("max_rating", lit(5))
        df_job_reviews = df_job_reviews.dropDuplicates()
        w_path = os.path.join(write_path, f"df_job_reviews_{self.source}.csv")
        df_job_reviews.toPandas().to_csv(w_path, index=False)
