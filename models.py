# models.py
from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WeatherSummary(Base):
    __tablename__ = 'weather_summary'

    id = Column(Integer, primary_key=True)
    city = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    avg_temp = Column(Float, nullable=False)
    max_temp = Column(Float, nullable=False)
    min_temp = Column(Float, nullable=False)
    dominant_weather = Column(String, nullable=False)

    def __repr__(self):
        return f"<WeatherSummary(city={self.city}, date={self.date}, avg_temp={self.avg_temp})>"
