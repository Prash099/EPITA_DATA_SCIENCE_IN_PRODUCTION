import pandas as pd
import requests
import json
import datetime
import os
from Py_Scripts import valid_output_great_expectations


def trigger_air_api():
    base_filename = datetime.datetime.now().strftime("%Y%m%d")

    for root, _, files in os.walk(valid_output_great_expectations):
        for filename in files:
            if filename.endswith('.csv'):
                csv_file_path = os.path.join(root, filename)
                
                data_file = pd.read_csv(csv_file_path)

                endpoint = 'http://127.0.0.1:8000/predict'
                headers = {"Content-Type": "application/json"}
                data_file = data_file.drop(['quality','Id'], axis =1)

                response = requests.post(endpoint, data=json.dumps(data_file.values.tolist()), headers=headers)
                if response.status_code == 200:
                    print("DAG triggered successfully.")
                else:
                    print("Failed to trigger DAG.")