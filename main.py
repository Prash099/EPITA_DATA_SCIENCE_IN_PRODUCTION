from fastapi import FastAPI
from math import gcd
from typing import List
from Py_Scripts.FeaturesInput import FeaturesInput
from Py_Scripts.UserInput import UserInput
from Py_Scripts.get_raw_wine_data import get_raw_wine_data
from Py_Scripts.get_past_predictions import get_past_predictions
from Py_Scripts.make_predictions import make_predictions


app = FastAPI()


@app.post("/calculate")
def operate(input: UserInput):
    result = gcd(input.x, input.y)
    return result


@app.post("/features_predict")
def operate(input: FeaturesInput):
    result = (input.fixed_acidity, input.volatile_acidity, input.citric_acid, input.residual_sugar, input.chlorides,
              input.free_sulfur_dioxide, input.total_sulfur_dioxide, input.density, input.pH, input.sulphates,
              input.alcohol)
    return result


@app.get("/read_raw_winedata")
def read_raw_winedata():
    try:
        wine_data_list = get_raw_wine_data()
        return {"wine_data_list": wine_data_list, "status_code": 200}
    except Exception as e:
        print(e.args)
        return {"wine_data_list": wine_data_list, "status_code": 500}


@app.post("/predict")
def predict(data: List):
    try:
        predictions = make_predictions(data)
        return {"Predictions": predictions, "status_code": 200}
    except Exception as e:
        print(e.args)
        return {"Predictions": [] , "status_code": 500}

@app.get("/past_predictions")
def past_predictions():
    try:
        prediction_list = get_past_predictions()
        return {"prediction_list": prediction_list, "status_code": 200}
    except Exception as e:
        print(e.args)
        return {"prediction_list": [], "status_code": 500}