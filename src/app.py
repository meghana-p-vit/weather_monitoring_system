import schedule
import time
import sqlite3
import datetime
import plotly.graph_objects as go
from flask import Flask, render_template
from weather_data import fetch_weather_data, update_daily_summary
from alert_system import check_alerts
from config import CITIES, FETCH_INTERVAL
from visualization import plot_daily_summary

app = Flask(__name__)

# Define alert levels
ALERT_LEVELS = {
    "Yellow": {"min_temp": 30, "max_temp": 35},
    "Red": {"min_temp": 35, "max_temp": 50},
}

# Set up SQLite connection
def init_db():
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    # Create the weather table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            date TEXT,
            city TEXT,
            temp REAL,
            feels_like REAL,
            weather TEXT,
            timestamp INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def store_weather_data(weather_data):
    """Store the weather data in SQLite database."""
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO weather (date, city, temp, feels_like, weather, timestamp) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (current_date, weather_data['city'], weather_data['temp'],
          weather_data['feels_like'], weather_data['weather'], weather_data['timestamp']))
    conn.commit()
    conn.close()

def update_weather_for_all_cities():
    """Fetch weather data for all cities and update the daily summary and alerts."""
    for city in CITIES:
        weather_data = fetch_weather_data(city)
        if weather_data:
            update_daily_summary(weather_data)
            check_alerts(weather_data)
            store_weather_data(weather_data)

def run_weather_monitoring():
    """Run the weather monitoring process and generate visualizations."""
    update_weather_for_all_cities()

    # Generate visualizations after updating the weather data
    for city in CITIES:
        plot_daily_summary(city)  # Plot weather data for each city

# Schedule the weather monitoring to run at the specified interval
schedule.every(FETCH_INTERVAL).seconds.do(run_weather_monitoring)

def fetch_historical_data(city):
    """Fetch historical weather data for the given city."""
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    c.execute("SELECT date, temp, feels_like, weather, timestamp FROM weather WHERE city = ?", (city,))
    rows = c.fetchall()
    conn.close()
    return rows

def fetch_all_weather_data():
    """Fetch all weather data from the database."""
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM weather")
    rows = c.fetchall()
    conn.close()
    return rows

@app.route('/')
def index():
    weather_data = fetch_all_weather_data()
    return render_template('index.html', weather_data=weather_data)

def plot_temperature_interactive(city):
    """Create an interactive temperature plot for the given city."""
    historical_data = fetch_historical_data(city)

    if not historical_data:
        print(f"No historical data found for {city}.")
        return

    dates = [datetime.datetime.strptime(record[0], '%Y-%m-%d') for record in historical_data]
    temperatures = [record[1] for record in historical_data]

    fig = go.Figure(data=[go.Scatter(x=dates, y=temperatures, mode='lines+markers', name=f'Temperature in {city}')])

    fig.update_layout(title=f'Temperature Trend for {city}',
                      xaxis_title='Date',
                      yaxis_title='Temperature (°C)',
                      xaxis=dict(tickformat='%Y-%m-%d'))
    fig.show()

if __name__ == "__main__":
    init_db()  # Initialize the database
    # Initial run to capture data immediately upon start
    run_weather_monitoring()
    app.run(debug=True)

    # Start the Flask app in a separate thread
    from threading import Thread
    Thread(target=lambda: app.run(debug=True)).start()

    # Continuously monitor weather data at the scheduled interval
    while True:
        schedule.run_pending()
        time.sleep(1)
