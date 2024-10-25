from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
from sqlalchemy.orm import sessionmaker
from db import engine  # Assuming you have db.py managing the database connection
from models import WeatherSummary  # Assuming WeatherSummary is your ORM model



# Initialize the session (if not already managed globally)
Session = sessionmaker(bind=engine)
session = Session()

def plot_daily_summary(city):
    # Query daily summaries from the database for the given city
    summaries = session.query(WeatherSummary).filter_by(city=city).all()

    # Check if any data is available
    if not summaries:
        print(f"No weather data available for {city}.")
        return

    # Extract dates and average temperatures from the query results
    dates = [datetime.strptime(s.date, "%Y-%m-%d") for s in summaries]
    avg_temps = [s.avg_temp for s in summaries]

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(dates, avg_temps, label='Average Temperature', marker='o', color='b')

    # Set plot title and labels
    plt.title(f"Daily Weather Summary for {city}", fontsize=16)
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Temperature (°C)', fontsize=14)

    # Format the x-axis with date ticks
    plt.gca().xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))  # Set interval for date ticks
    plt.gcf().autofmt_xdate()  # Rotate date labels for better readability

    # Add grid and legend
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()

    # Show the plot
    plt.tight_layout()  # Adjust layout to prevent clipping of labels
    plt.show()

