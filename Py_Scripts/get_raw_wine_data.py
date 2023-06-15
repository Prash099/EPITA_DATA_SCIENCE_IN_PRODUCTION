import pandas as pd
from sqlalchemy import Column, String, create_engine
from Py_Scripts.WineData import WineData
from fastapi.responses import JSONResponse


class WineDataWithTimestamp(WineData):
    created_at_formatted: str


def get_raw_wine_data(session):
    try:
        wine_data_list = []
        result = session.query(WineData).all()

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
                "quality": item.quality,
                "created_at": item.created_at
            }
            
            wine_data_list.append(wine_dict)
        
        session.close()
        df = pd.DataFrame(wine_data_list)
        return {"data": df.to_json(orient="records"), "status": 200}    
    
    except Exception as e:
        print(e.args)
        return {"data": {}, 'status': 500}
