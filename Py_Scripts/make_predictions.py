from typing import List
import pandas as pd
from Py_Scripts.save_predictions_to_database import save_predictions_to_database
from Py_Scripts.load_constants import load_constants
from fastapi.responses import JSONResponse


def make_predictions(session: bytes, data: List):
    model, features, scaler = load_constants()
    data = pd.DataFrame(data, columns=list(features))
    scaled_features_df = pd.DataFrame(scaler.transform(data), columns=list(features))

    prediction = model.predict(scaled_features_df)
    data['predicted_quality'] = list(prediction)

    save_predictions_to_database(session, data.values.tolist())
    return JSONResponse(content=data.to_json(orient="records"), status_code=200)