import requests
import json
import os
from datetime import datetime
from collections import Counter
from config import API_KEY, CITIES, TEMP_UNIT

# Path for the summary file
SUMMARY_FILE = 'daily_summary.json'

def kelvin_to_celsius(temp):
    return temp - 273.15

def kelvin_to_fahrenheit(temp):
    return (temp - 273.15) * 9/5 + 32

def fetch_weather_data(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=h3hf874ir72jf0qd3bd7c3a0ng6f9nb3"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()

        # Extract necessary data from the response
        temp_kelvin = data['main']['temp']
        feels_like_kelvin = data['main']['feels_like']
        weather_condition = data['weather'][0]['description']  # Change to description
        timestamp = data['dt']

        # Convert temperature based on the specified unit
        if TEMP_UNIT == "Celsius":
            temp = kelvin_to_celsius(temp_kelvin)
            feels_like = kelvin_to_celsius(feels_like_kelvin)
        else:
            temp = kelvin_to_fahrenheit(temp_kelvin)
            feels_like = kelvin_to_fahrenheit(feels_like_kelvin)

        return {
            "city": city,
            "temp": round(temp, 2),  # Round to 2 decimal places
            "feels_like": round(feels_like, 2),
            "weather": weather_condition,
            "timestamp": timestamp
        }

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Error occurred: {req_err}")
    except KeyError as key_err:
        print(f"Missing data in the response: {key_err}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")

    return None  # Return None if there was an error
def update_daily_summary(weather_data):
    # Create a summary entry
    summary_entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "weather": weather_data
    }

    # Check if the summary file exists and load existing data
    if os.path.exists(SUMMARY_FILE):
        with open(SUMMARY_FILE, 'r') as file:
            summaries = json.load(file)
    else:
        summaries = []

    # Add new summary entry
    summaries.append(summary_entry)

    # Save updated summaries back to the file
    with open(SUMMARY_FILE, 'w') as file:
        json.dump(summaries, file, indent=4)

    print(f"Updated daily summary: {summary_entry}")

def get_summary_for_day(date):
    """Fetch summary for a specific date."""
    if os.path.exists(SUMMARY_FILE):
        with open(SUMMARY_FILE, 'r') as file:
            summaries = json.load(file)
            for entry in summaries:
                if entry['date'] == date:
                    return entry
    return None

def save_daily_summary(date, city, avg_temp, max_temp, min_temp, dominant_weather):
    """Save daily summary with aggregated data."""
    summary_entry = {
        "date": date,
        "city": city,
        "average_temperature": avg_temp,
        "maximum_temperature": max_temp,
        "minimum_temperature": min_temp,
        "dominant_weather": dominant_weather
    }

    # Check if the summary file exists and load existing data
    if os.path.exists(SUMMARY_FILE):
        with open(SUMMARY_FILE, 'r') as file:
            summaries = json.load(file)
    else:
        summaries = []

    # Add or update the summary entry
    summaries.append(summary_entry)

    # Save updated summaries back to the file
    with open(SUMMARY_FILE, 'w') as file:
        json.dump(summaries, file, indent=4)

    print(f"Saved daily summary for {city} on {date}: {summary_entry}")

def calculate_daily_summary(date, city):
    """Calculate daily summary including avg, min, max temperatures and dominant weather."""
    if os.path.exists(SUMMARY_FILE):
        with open(SUMMARY_FILE, 'r') as file:
            summaries = json.load(file)

        # Filter data for the given date and city
        day_data = [entry['weather'] for entry in summaries if entry['date'] == date and entry['weather']['city'] == city]


        if day_data:
            temps = [data['temp'] for data in day_data]
            weather_conditions = [data['weather'] for data in day_data]

            avg_temp = round(sum(temps) / len(temps), 2)
            max_temp = round(max(temps), 2)
            min_temp = round(min(temps), 2)
            dominant_weather = Counter(weather_conditions).most_common(1)[0][0]  # Find most common weather condition

            save_daily_summary(date, city, avg_temp, max_temp, min_temp, dominant_weather)
        else:
            print(f"No data available for {city} on {date}")
    else:
        print("No summary data found.")

# Example usage: calculating and saving daily summaries for all cities
def update_weather_for_all_cities():
    """Fetch weather data for all cities and update the daily summary and alerts."""
    for city in CITIES:
        weather_data = fetch_weather_data(city)
        if weather_data:
            update_daily_summary(weather_data)  # Make sure this function saves the data correctly
            check_alerts(weather_data)           # Check alerts for this weather data
            store_weather_data(weather_data)     # Store the data in SQLite

if __name__ == "__main__":
    update_weather_for_all_cities()
