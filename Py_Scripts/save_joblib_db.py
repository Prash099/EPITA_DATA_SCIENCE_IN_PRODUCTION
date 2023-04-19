import psycopg2
import joblib
import pickle

DB_HOST = "localhost"
DB_NAME = "WINE_DB"
DB_USER = "postgres"
DB_PASSWORD = "root321"

# Establish connection with the PostgreSQL database
conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# Define a cursor object
cur = conn.cursor()

# Serialize joblib objects to bytes
model_obj = joblib.load('../Model/model.joblib')
model_obj_bytes = pickle.dumps(model_obj)

feature_obj = joblib.load('../Model/features.joblib')
feature_obj_bytes = pickle.dumps(feature_obj)

scaler_obj = joblib.load('../Model/scaler.joblib')
scaler_obj_bytes = pickle.dumps(scaler_obj)

cur.execute("INSERT INTO constants (name, value) VALUES (%s, %s)", ("model", model_obj_bytes))
cur.execute("INSERT INTO constants (name, value) VALUES (%s, %s)", ("features", feature_obj_bytes))
cur.execute("INSERT INTO constants (name, value) VALUES (%s, %s)", ("scaler", scaler_obj_bytes))

conn.commit()

cur.close()
conn.close()
