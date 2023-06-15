import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class WineDataPrediction(Base):
    __tablename__ = 'wine_prediction_result'

    id = Column(Integer, primary_key=True)
    fixed_acidity = Column(Float)
    volatile_acidity = Column(Float)
    citric_acid = Column(Float)
    residual_sugar = Column(Float)
    chlorides = Column(Float)
    free_sulfur_dioxide = Column(Float)
    total_sulfur_dioxide = Column(Float)
    density = Column(Float)
    ph = Column(Float)
    sulphates = Column(Float)
    alcohol = Column(Float)
    predicted_quality = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<WineDataPrediction(id={self.id}, predicted_quality={self.predicted_quality})>"
