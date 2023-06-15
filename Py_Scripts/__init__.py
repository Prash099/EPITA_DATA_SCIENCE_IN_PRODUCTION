DB_HOST = "localhost"
DB_NAME = "WINE_DB"
DB_USER = "postgres"
DB_PASSWORD = "1106"
DB_PORT = "5432"

MODEL_PATH = "Model/model.joblib"
FEATURE_PATH = "Model/features.joblib"
SCALAR_PATH = "Model/scaler.joblib"

input_file_great_expectations = '/Users/kiruba/Documents/GitHub/EPITA_DATA_SCIENCE_IN_PRODUCTION/airflow/data/Clean_Data'
output_directory_great_expectations = '/Users/kiruba/Documents/GitHub/EPITA_DATA_SCIENCE_IN_PRODUCTION/airflow/data/Split_Data'
invalid_output_file_great_expectations = '/Users/kiruba/Documents/GitHub/EPITA_DATA_SCIENCE_IN_PRODUCTION/airflow/data/Invalid_Data'
valid_output_great_expectations = '/Users/kiruba/Documents/GitHub/EPITA_DATA_SCIENCE_IN_PRODUCTION/airflow/data/Valid_Data'

value_ranges = {
    'fixed acidity': (4.6, 15.9),
    'volatile acidity': (0.12, 1.58),
    'citric acid': (0.0, 1.0),
    'residual sugar': (0.9, 15.5),
    'chlorides': (0.012, 0.611),
    'free sulfur dioxide': (1.0, 68.0),
    'total sulfur dioxide': (6.0, 289.0),
    'density': (0.99007, 1.00369),
    'pH': (2.74, 4.01),
    'sulphates': (0.33, 2.0),
    'alcohol': (8.4, 14.9)
}