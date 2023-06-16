from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from great import great_expectations_validation
from Py_Scripts import input_file_great_expectations, output_directory_great_expectations,invalid_output_file_great_expectations,valid_output_great_expectations
from trigger_air_api import trigger_air_api


def my_python_function():
    great_expectations_validation(input_file_great_expectations, output_directory_great_expectations, invalid_output_file_great_expectations, valid_output_great_expectations)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 6, 15),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG('great_expectation_folder', default_args=default_args, schedule_interval='*/5 * * * *') as dag:
    t1 = PythonOperator(task_id='great_expectation_folder_task', python_callable=my_python_function, dag=dag)
    t2 = PythonOperator(task_id='trigger_fastapi_task', python_callable=trigger_air_api, dag=dag)
    t1 >> t2
