import pandas as pd
import requests
import json
import datetime
import os


def trigger_air_api():
    folder_path = '/Users/kiruba/Documents/GitHub/EPITA_DATA_SCIENCE_IN_PRODUCTION/airflow/data/Valid_Data'

    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path) 
            endpoint = 'http://127.0.0.1:8000/predict'
            headers = {"Content-Type": "application/json"}
            data_file = df.drop(['quality','Id'], axis =1)

            response = requests.post(endpoint, data=json.dumps(data_file.values.tolist()), headers=headers)
            if response.status_code == 200:
                print("DAG triggered successfully.")
            else:
                print("Failed to trigger DAG.")
                    
# trigger_air_api()