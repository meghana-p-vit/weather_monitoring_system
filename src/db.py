from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class WeatherSummary(Base):
    __tablename__ = 'weather_summary'
    id = Column(Integer, primary_key=True)
    city = Column(String)
    avg_temp = Column(Float)
    max_temp = Column(Float)
    min_temp = Column(Float)
    dominant_weather = Column(String)
    date = Column(DateTime, default=datetime.utcnow)

# Database setup
engine = create_engine('sqlite:///weather_data.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
