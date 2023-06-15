import joblib
from Py_Scripts import MODEL_PATH, FEATURE_PATH, SCALAR_PATH

def load_constants():
    try:
        model_obj = joblib.load(MODEL_PATH)
        feature_obj = joblib.load(FEATURE_PATH)
        scaler_obj = joblib.load(SCALAR_PATH)
        return model_obj, feature_obj, scaler_obj
    except Exception as e:
        print(e.args)
        return [], [], []
    