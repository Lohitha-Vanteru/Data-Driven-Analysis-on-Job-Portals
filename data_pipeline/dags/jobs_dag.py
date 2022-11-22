"""Main DAG"""

from datetime import datetime, timedelta
import os

from airflow import DAG
from airflow.utils.dates import days_ago

from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

from operators.copy_redshift import CopyToRedshiftOperator
from operators.data_quality import DataQualityOperator


args = {
    'owner': 'Theinsightco',
    'start_date': days_ago(2),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_retry': False,
    'email': "lohitha.vanteru@sjsu.edu"
}

template_search_path = os.getenv("AIRFLOW_HOME")

dag = DAG(
    dag_id='jobs_analysis',
    description='Process data from multiple job soruces, transform data and push it to tables used by recruitment team',
    default_args=args,
    schedule_interval='0 0 * * *',
    template_searchpath = [template_search_path],
    dagrun_timeout=timedelta(minutes=60),
)


start_operator = DummyOperator(task_id='Start_Execution',  dag=dag)

process_data_lake = BashOperator(
    task_id='Process_Data_Lake',
    bash_command='process-data-from-lake',
    dag=dag)

create_tables = PostgresOperator(task_id='Create_Tables', 
                                 dag=dag, 
                                 postgres_conn_id="redshift_tci", 
                                 sql="create_tables.sql")

copy_jobs_to_redshift = CopyToRedshiftOperator(
    task_id='Copy_Jobs_Details',
    dag=dag,
    table="jobs",
    redshift_conn_id="redshift_tci",
    aws_credentials_id="aws_default",
    s3_bucket="jobscleandata",
    s3_key="jobs_table/",
    format_type="csv"
)


copy_company_location_to_redshift = CopyToRedshiftOperator(
    task_id='Copy_Company_location_Details',
    dag=dag,
    table="company_location",
    redshift_conn_id="redshift_tci",
    aws_credentials_id="aws_default",
    s3_bucket="jobscleandata",
    s3_key="company_location/",
    format_type="csv"
)


copy_job_rating_to_redshift = CopyToRedshiftOperator(
    task_id='Copy_Job_Ratings_Details',
    dag=dag,
    table="job_rating",
    redshift_conn_id="redshift_tci",
    aws_credentials_id="aws_default",
    s3_bucket="jobscleandata",
    s3_key="job_reviews/",
    format_type="csv"
)


copy_job_sector_to_redshift = CopyToRedshiftOperator(
    task_id='Copy_Job_Sector_Details',
    dag=dag,
    table="job_sector",
    redshift_conn_id="redshift_tci",
    aws_credentials_id="aws_default",
    s3_bucket="jobscleandata",
    s3_key="job_sector/",
    format_type="csv"
)


copy_job_salary_to_redshift = CopyToRedshiftOperator(
    task_id='Copy_Job_Salaries_Details',
    dag=dag,
    table="job_salary",
    redshift_conn_id="redshift_tci",
    aws_credentials_id="aws_default",
    s3_bucket="jobscleandata",
    s3_key="job_salary/",
    format_type="csv"
)


copy_employees_to_redshift = CopyToRedshiftOperator(
    task_id='Copy_employees_Details',
    dag=dag,
    table="employees",
    redshift_conn_id="redshift_tci",
    aws_credentials_id="aws_default",
    s3_bucket="jobscleandata",
    s3_key="employee_details/",
    format_type="csv"
)


dq_null_checks = [
{'check_sql': "SELECT COUNT(*) FROM jobs;", 'test_expr': "{} < 1"},
{'check_sql': "SELECT COUNT(*) FROM employees WHERE person_id is NULL;", 'test_expr': "{} >= 1"}
]

count_and_null_test = DataQualityOperator(
    task_id='Count_and_Null_Test',
    dag=dag,
    redshift_conn_id="redshift_tci",
    dq_checks=dq_null_checks
)


dq_join_checks = [
{'check_sql': "SELECT COUNT(*) FROM job_salary JOIN company_location on (job_salary.company = company_location.company);", 'test_expr': "{} < 1"},
]

table_relation_test = DataQualityOperator(
    task_id='Table_Relation_Test',
    dag=dag,
    redshift_conn_id="redshift_tci",
    dq_checks=dq_join_checks
)


end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

# Setting tasks direction
start_operator >> process_data_lake
process_data_lake >> create_tables

create_tables >> copy_jobs_to_redshift
create_tables >> copy_company_location_to_redshift
create_tables >> copy_job_rating_to_redshift
create_tables >> copy_job_sector_to_redshift
create_tables >> copy_job_salary_to_redshift
create_tables >> copy_employees_to_redshift


copy_jobs_to_redshift >> count_and_null_test
copy_company_location_to_redshift >> count_and_null_test
copy_job_rating_to_redshift >> count_and_null_test
copy_job_sector_to_redshift >> count_and_null_test
copy_job_salary_to_redshift >> count_and_null_test
copy_employees_to_redshift >> count_and_null_test


copy_jobs_to_redshift >> table_relation_test
copy_company_location_to_redshift >> table_relation_test
copy_job_rating_to_redshift >> table_relation_test
copy_job_sector_to_redshift >> table_relation_test
copy_job_salary_to_redshift >> table_relation_test
copy_employees_to_redshift >> table_relation_test


count_and_null_test >> end_operator
table_relation_test >> end_operator
