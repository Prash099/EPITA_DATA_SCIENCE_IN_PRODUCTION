import joblib

DB_HOST = "localhost"
DB_NAME = "WINE_DB"
DB_USER = "postgres"
DB_PASSWORD = "1106"

def load_constants():
    try:
        model_obj = joblib.load("/Users/kiruba/Documents/GitHub/EPITA_DATA_SCIENCE_IN_PRODUCTION/Model/model.joblib")
        feature_obj = joblib.load("/Users/kiruba/Documents/GitHub/EPITA_DATA_SCIENCE_IN_PRODUCTION/Model/features.joblib")
        scaler_obj = joblib.load("/Users/kiruba/Documents/GitHub/EPITA_DATA_SCIENCE_IN_PRODUCTION/Model/scaler.joblib")
        return model_obj, feature_obj, scaler_obj
    except Exception as e:
        print(e.args)
        return [], [], []