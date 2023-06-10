from Py_Scripts.WineDataPrediction import WineDataPrediction

def save_predictions_to_database(session, predictions):
    try:
        if isinstance(predictions, float):
            predictions = [predictions]

        for values in predictions:
            prediction = WineDataPrediction(
                fixed_acidity=values[0],
                volatile_acidity=values[1],
                citric_acid=values[2],
                residual_sugar=values[3],
                chlorides=values[4],
                free_sulfur_dioxide=values[5],
                total_sulfur_dioxide=values[6],
                density=values[7],
                ph=values[8],
                sulphates=values[9],
                alcohol=values[10],
                predicted_quality=values[11]
            )
            session.add(prediction)

        session.commit()
        session.close()

        return {"status": 200}
    except Exception as e:
        print(e.args)
        return {"status": 500}
