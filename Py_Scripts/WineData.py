from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class WineData(Base):
    __tablename__ = 'wine_data_raw'

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
    quality = Column(Integer)
    created_at = Column(DateTime)

    def __repr__(self):
        return f"<WineData(id={self.id}, quality={self.quality})>"