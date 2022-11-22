import os
from pyspark.sql.functions import col
from pyspark.sql.functions import lit
from pyspark.sql.functions import lower
from pyspark.sql.functions import udf
from data_lake.data_util import DataUtil

#Employee survey data transform module
class Employee(DataUtil):
    def __init__(self, spark_session, source_path):
        super().__init__(spark_session)
        self.source = "stackoverflow"
        self.source_path = source_path
    #Generate data for employeesurvey table
    def generate_employeesurvey_details(self, write_path):
        #Replace column names
        resp_cols = ["Respondent as person_id", "Hobby as hobby","OpenSource as open_source_contrib",  "Country as country", "Student as student",  "Employment as employment", "FormalEducation as main_education", "DevType as development_area", "LastNewJob as latest_job",  "TimeFullyProductive as productive_hours", "Gender as gender", "Age as age"]
        df_es = self.main_df.selectExpr(*resp_cols)
        w_path = os.path.join(write_path, f"df_devloper_{self.source}.csv")
        df_es.toPandas().to_csv(w_path, index=False)