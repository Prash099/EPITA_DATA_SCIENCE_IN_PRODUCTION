import psycopg2
import base64
import joblib

DB_HOST = "localhost"
DB_NAME = "WINE_DB"
DB_USER = "postgres"
DB_PASSWORD = "root321"

def load_constants():
    try:
        model_obj = joblib.load("Model/model.joblib")
        feature_obj = joblib.load("Model/features.joblib")
        scaler_obj = joblib.load("Model/scaler.joblib")
        return model_obj, feature_obj, scaler_obj
    except Exception as e:
        print(e.args)
        return [], [], []



# conn = psycopg2.connect(
    #     host=DB_HOST,
    #     database=DB_NAME,
    #     user=DB_USER,
    #     password=DB_PASSWORD
    # )

    # cur = conn.cursor()

    # cur.execute("SELECT * FROM constants")
    # rows = cur.fetchall()

    # model_obj_bytes = None
    # feature_obj_bytes = None
    # scaler_obj_bytes = None

    # for row in rows:
    #     name = row[0]
    #     value = row[1]

    #     while len(value) % 4 != 0:
    #         value += "="

    #     # decode the data
    #     value = base64.b64decode(value)

    #     if name == "model":
    #         model_obj_bytes = value.encode('utf-8')
    #     elif name == "features":
    #         feature_obj_bytes = base64.b64decode(value.encode('utf-8'))
    #     elif name == "scaler":
    #         scaler_obj_bytes = base64.b64decode(value.encode('utf-8'))

    # cur.close()
    # conn.close()

    # model_obj = joblib.load(model_obj_bytes)
    # feature_obj = joblib.load(feature_obj_bytes)
    # scaler_obj = joblib.load(scaler_obj_bytes)
