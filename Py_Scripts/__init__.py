DB_HOST = "localhost"
DB_NAME = "WINE_DB"
DB_USER = "postgres"
DB_PASSWORD = "root321"
DB_PORT = "5432"

MODEL_PATH = "Model/model.joblib"
FEATURE_PATH = "Model/features.joblib"
SCALAR_PATH = "Model/scaler.joblib"

INSERT_WINE_PREDICTION_QUERY = """
                    INSERT INTO WINE_PREDICTION_RESULT (fixed_acidity, volatile_acidity,
                    citric_acid, residual_sugar, chlorides, free_sulfur_dioxide, 
                    total_sulfur_dioxide, density, pH, sulphates, alcohol, predicted_quality)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """

SELECT_WINE_PREDICTION_RESULT_QUERY = """
                        SELECT id, fixed_acidity, volatile_acidity, citric_acid, 
                        residual_sugar, chlorides, free_sulfur_dioxide, 
                        total_sulfur_dioxide, density, ph, sulphates, alcohol, predicted_quality, 
                        created_at, to_char(created_at, 'YYYY-MM-DD HH24:MI:SS.US') 
                        FROM WINE_PREDICTION_RESULT
                       """

SELECT_WINE_DB_RAW_QUERY = """
                        SELECT id, fixed_acidity, volatile_acidity, citric_acid, 
                        residual_sugar, chlorides, free_sulfur_dioxide, total_sulfur_dioxide, 
                        density, ph, sulphates, alcohol, quality, 
                        created_at, to_char(created_at, 'YYYY-MM-DD HH24:MI:SS.US') 
                        FROM WINE_DATA_RAW LIMIT 5
                       """