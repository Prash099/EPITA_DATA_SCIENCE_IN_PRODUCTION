import pandas as pd
import requests
import json
import datetime
import time

def trigger_air_api():
    time.sleep(10)
    base_filename = str(datetime.datetime.now().strftime("%Y%m%d"))
    data_file = pd.read_csv("/Users/kiruba/Documents/GitHub/EPITA_DATA_SCIENCE_IN_PRODUCTION/airflow/20230615.csv")

    endpoint = 'http://127.0.0.1:8000/predict'
    headers = {"Content-Type": "application/json"}
    data_file = data_file.drop(['quality','Id'], axis =1)

    response = requests.post(endpoint, data=json.dumps(data_file.values.tolist()), headers=headers)
    if response.status_code == 200:
        print("DAG triggered successfully.")
    else:
        print("Failed to trigger DAG.")