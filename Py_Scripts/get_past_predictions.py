import pandas as pd
from fastapi.responses import JSONResponse
from Py_Scripts.WineDataPrediction import WineDataPrediction
import psycopg2

DB_HOST = "localhost"
DB_NAME = "WINE_DB"
DB_USER = "postgres"
DB_PASSWORD = "root321"


class WineDataWithTimestamp(WineDataPrediction):
    created_at_formatted: str


def get_past_predictions():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()
    cur.execute("SELECT id, fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides, free_sulfur_dioxide, total_sulfur_dioxide, density, ph, sulphates, alcohol, predicted_quality, created_at, to_char(created_at, 'YYYY-MM-DD HH24:MI:SS.US') FROM WINE_PREDICTION_RESULT")
    rows = cur.fetchall()
    wine_data_list = []
    for row in rows:
        wine_dict = {
            "id": row[0],
            "fixed_acidity": row[1],
            "volatile_acidity": row[2],
            "citric_acid": row[3],
            "residual_sugar": row[4],
            "chlorides": row[5],
            "free_sulfur_dioxide": row[6],
            "total_sulfur_dioxide": row[7],
            "density": row[8],
            "ph": row[9],
            "sulphates": row[10],
            "alcohol": row[11],
            "predicted_quality": row[12],
            "created_at": row[13],
            "created_at_formatted": row[14]
        }
        wine_data = WineDataWithTimestamp(**wine_dict)
        wine_data_list.append(wine_data)

    cur.close()
    conn.close()

    df = pd.DataFrame([wine.dict() for wine in wine_data_list])
    return JSONResponse(content=df.to_json(orient="records"), status_code=200)
