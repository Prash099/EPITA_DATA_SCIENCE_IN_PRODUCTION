from fastapi import FastAPI
from typing import List
from Py_Scripts.get_raw_wine_data import get_raw_wine_data
from Py_Scripts.get_past_predictions import get_past_predictions
from Py_Scripts.make_predictions import make_predictions
from Py_Scripts.db_engine import db_engine

app = FastAPI()

@app.get("/read_raw_winedata")
def read_raw_winedata():
    try:
        database = db_engine()
        wine_data_list = get_raw_wine_data(database['session'])
        return {"wine_data_list": wine_data_list['data'], "status": wine_data_list['status']}
    except Exception as e:
        print(e.args)
        return {"wine_data_list": wine_data_list['data'], "status": wine_data_list['status']}


@app.post("/predict")
def predict(data: List):
    try:
        database = db_engine()
        predictions = make_predictions(database['session'], data)
        return {"Predictions": predictions, "status_code": 200}
    except Exception as e:
        print(e.args)
        return {"Predictions": [] , "status_code": 500}

@app.get("/past_predictions")
def past_predictions():
    try:
        database = db_engine()
        prediction_list = get_past_predictions(database['session'])
        return {"prediction_list": prediction_list['data'], "status": prediction_list['status']}
    except Exception as e:
        print(e.args)
        return {"prediction_list": [], "status": prediction_list['status']}