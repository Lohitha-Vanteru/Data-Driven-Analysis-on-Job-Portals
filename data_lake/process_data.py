#Project Entry point

import configparser
import os

from data_lake.glassdoor_jobs import GlassdoorJobs
from data_lake.indeed_jobs import IndeedJobs
from data_lake.linkedin_jobs import LinkedInJobs
from data_lake.employee_survey import Employee
from data_lake.techmapjobs import TechmapJobs
from data_lake.DiceJobs import DiceJobs
from data_lake.Monsterjobs import MonsterJobs
from data_lake.ziprecruiter import ZiprecruiterJobs
from pyspark.sql import SparkSession

#Creates Spark Session in Local Mode
def create_spark_session():
    spark = SparkSession.builder.config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4").getOrCreate()
    return spark

#Process data coming from Multiple Sources
#s_paths (dict): A dictionary with source name and its path
#w_paths (dict): A dictionary with destination name and its path
def etl(spark, s_paths, w_paths):
    l = LinkedInJobs(spark, source_path=s_paths["LINKEDIN_PATH"])
    l.read_data_from_source()
    l.generate_jobs_table(w_paths["JOBS_TABLE"])
    l.generate_location_description(w_paths["LOCATION_TABLE"])                       
        
    i = IndeedJobs(spark, source_path=s_paths["INDEED_PATH"])
    i.read_data_from_source()
    i.generate_jobs_table(w_paths["JOBS_TABLE"])
    i.generate_location_description(w_paths["LOCATION_TABLE"])
    i.generate_job_reviews(w_paths["JOB_REVIEWS"])

    g = GlassdoorJobs(spark, source_path=s_paths["GLASSDOOR_PATH"])
    g.read_data_from_source()
    g.generate_jobs_table(w_paths["JOBS_TABLE"])
    g.generate_location_description(w_paths["LOCATION_TABLE"])
    g.generate_job_reviews(w_paths["JOB_REVIEWS"])
    g.generate_job_salary(w_paths["JOB_SALARY"])
    g.generate_job_sector(w_paths["JOB_SECTOR"])
        
    s = Employee(spark, source_path=s_paths["STACKOVERFLOW_PATH"])
    s.read_data_from_source()
    s.generate_employeesurvey_details(w_paths["EMPLOYEE_DETAILS"])
    

    d=DiceJobs(spark, source_path=s_paths["DICE_PATH"])
    d.read_data_from_source()
    d.generate_jobs_table(w_paths["JOBS_TABLE"])
    d.generate_location_description(w_paths["LOCATION_TABLE"])
    d.generate_job_sector(w_paths["JOB_SECTOR"])

    m=MonsterJobs(spark, source_path=s_paths["MONSTER_PATH"])
    m.read_data_from_source()
    m.generate_jobs_table(w_paths["JOBS_TABLE"])
    m.generate_location_description(w_paths["LOCATION_TABLE"])
    m.generate_job_sector(w_paths["JOB_SECTOR"])

    z=ZiprecruiterJobs(spark, source_path=s_paths["ZIPRECRUITER_PATH"])
    z.read_data_from_source()
    z.generate_jobs_table(w_paths["JOBS_TABLE"])
    z.generate_location_description(w_paths["LOCATION_TABLE"])
    z.generate_job_sector(w_paths["JOB_SECTOR"])

#Main Entry Function
def main():
    config_path = "/home/ubuntu/theinsightco_project/data_lake/lake.cfg"
    config = configparser.ConfigParser()
    config.read(config_path)
    print(config_path)

    os.environ['AWS_ACCESS_KEY_ID']=config["AWS"]['AWS_ACCESS_KEY_ID']
    os.environ['AWS_SECRET_ACCESS_KEY']=config["AWS"]['AWS_SECRET_ACCESS_KEY']

    spark = create_spark_session()
    etl(spark, config["SOURCE_PATH"], config["WRTIE_PATH"])
    spark.stop()

if __name__ == "__main__":
    main()
