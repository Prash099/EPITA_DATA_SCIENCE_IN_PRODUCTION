import pandas as pd
from Py_Scripts.WineDataPrediction import WineDataPrediction


def get_past_predictions(session):
    try:
        past_predictions = []
        result = session.query(WineDataPrediction).all()
        for item in result:
            wine_dict = {
                "id": item.id,
                "fixed_acidity": item.fixed_acidity,
                "volatile_acidity": item.volatile_acidity,
                "citric_acid": item.citric_acid,
                "residual_sugar": item.residual_sugar,
                "chlorides": item.chlorides,
                "free_sulfur_dioxide": item.free_sulfur_dioxide,
                "total_sulfur_dioxide": item.total_sulfur_dioxide,
                "density": item.density,
                "ph": item.ph,
                "sulphates": item.sulphates,
                "alcohol": item.alcohol,
                "predicted_quality": item.predicted_quality,
                "created_at": item.created_at
            }
            
            past_predictions.append(wine_dict)
            session.close()
        df = pd.DataFrame(past_predictions)
        return {"data": df.to_json(orient="records"), "status": 200}
            
    except Exception as e:
        print(e.args)
        return {"data": {}, 'status': 500}
