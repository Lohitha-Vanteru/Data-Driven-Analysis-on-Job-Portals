from pyspark.sql.functions import col
from pyspark.sql.functions import lit
from pyspark.sql.functions import lower
from pyspark.sql.functions import udf
from data_lake.data_util import DataUtil

#Techmap global jobs data transform module
class TechmapJobs(DataUtil):
    def __init__(self, spark_session, source_path):
        super().__init__(spark_session)
        self.source = "techmap"
        self.source_path = source_path
    #Generate data for jobs table
    def generate_jobs_table(self, write_path):
        df_jobs = self.main_df.select(col("name").alias("job_title"), col("Job Description").alias("position.workType"), col("orgCompany.name").alias("company"), col("orgAdress.city").alias("location"), )
        #converting all the job titles to lower case
        df_jobs = df_jobs.withColumn("job_title", lower(df_jobs.job_title))
        #adding column to display source of job
        df_jobs = df_jobs.withColumn("source", df_jobs.source)
        w_path = os.path.join(write_path, f"df_jobs_{self.source}.csv")
        df_jobs.toPandas().to_csv(w_path, index=False)
     #Generate data for company_location table
    def generate_location_description(self, write_path):
        df_job_location = self.main_df.select(col("orgCompany.name").alias("company"), col("orgAdress.city").alias("city"), col("orgAdress.state").alias("state"), col("orgAdress.country").alias("country"))
        df_job_location = df_job_location.withColumn("city",df_job_location.city )
        df_job_location = df_job_location.withColumn("state", df_job_location.state)
        df_job_location = df_job_location.withColumn("country", df_job_location.country)
        df_job_location = df_job_location.dropDuplicates()
        w_path = os.path.join(write_path, f"df_job_location_{self.source}.csv")
        df_job_location.toPandas().to_csv(w_path, index=False)
    #Generate data for job_salary table
    def generate_job_salary(self, write_path):
        df_job_salary = self.main_df.select(col("name").alias("job_title"), col("orgCompany.name").alias("company"), col("salary.text").alias("estimated_salary"))
        #getting estimated salary by removing extra information
        df_job_salary = df_job_salary.withColumn("estimated_salary", self.get_est_salary(df_job_salary.estimated_salary))
        df_job_salary = df_job_salary.dropDuplicates()
        w_path = os.path.join(write_path, f"df_job_salary_{self.source}.csv")
        df_job_salary.toPandas().to_csv(w_path, index=False)
    #Generate data for job_sector table
    def generate_job_sector(self, write_path):
        df_job_sector = self.main_df.select(col("name").alias("job_title"), col("position.department").alias("sector"))
        df_job_sector = df_job_sector.dropDuplicates()
        w_path = os.path.join(write_path, f"df_job_sectors_{self.source}.csv")
        df_job_sector.toPandas().to_csv(w_path, index=False)    
