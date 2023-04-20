import psycopg2

def save_predictions_to_database(predictions):
    try:
        if isinstance(predictions, float):
            predictions_json = [predictions]
        else:
            predictions_json = predictions
            
        conn = psycopg2.connect(
            host="localhost",
            database="WINE_DB",
            user="postgres",
            password="1106"
        )
        cur = conn.cursor()
        for prediction in predictions_json:
            cur.execute(
                """INSERT INTO WINE_PREDICTION_RESULT (fixed_acidity, volatile_acidity, \
                citric_acid, residual_sugar, chlorides, free_sulfur_dioxide, 
                total_sulfur_dioxide, density, pH, sulphates, alcohol, predicted_quality) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    prediction[0],
                    prediction[1],
                    prediction[2],
                    prediction[3],
                    prediction[4],
                    prediction[5],
                    prediction[6],
                    prediction[7],
                    prediction[8],
                    prediction[9],
                    prediction[10],
                    prediction[11]
                )
            )

        conn.commit()
        cur.close()
        conn.close()

        return {"status": 200}
    except Exception as e:
        print(e.args)
        return {"status": 500}
