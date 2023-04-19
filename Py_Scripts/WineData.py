from pydantic import BaseModel
from decimal import Decimal
import datetime

class WineData(BaseModel):
    id: int
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    ph: float
    sulphates: float
    alcohol: float
    quality: int
    created_at: datetime.datetime

    class Config:
        json_encoders = {
            Decimal: float,
            datetime.datetime: lambda dt: dt.strftime('%Y-%m-%d')
        }
