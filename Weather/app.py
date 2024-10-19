import streamlit as st
import requests
import pandas as pd
import sqlite3
from datetime import datetime
import time

# Custom CSS for colorful design
def add_custom_css():
    st.markdown("""
        <style>
            /* Background and font colors */
            body {
                background-color: #f0f4f7;
                color: #333;
                font-family: 'Arial', sans-serif;
            }
            
            /* Sidebar styling */
            .css-1d391kg {
                background-color: #404e5a;
                color: white;
            }
            
            /* Sidebar text */
            .css-1lcbmhc {
                color: white !important;
            }

            /* Title style */
            .css-10trblm {
                color: #1c87c9;
            }

            /* Input boxes, buttons */
            .stNumberInput, .stDataFrame, .stTextInput {
                background-color: #f7f9fc;
                color: #333;
            }

            /* Buttons */
            .stButton button {
                background-color: #1c87c9;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 8px;
                transition: background-color 0.3s ease;
            }
            .stButton button:hover {
                background-color: #14557b;
            }

            /* Dataframe styling */
            .stDataFrame table {
                background-color: white;
                border-radius: 10px;
                overflow: hidden;
            }

            /* General headings */
            h1, h2, h3 {
                color: #14557b;
            }
        </style>
    """, unsafe_allow_html=True)

# Constants
API_KEY = '4076d6495f397578438ab1767775fa54'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}'
FORECAST_URL = 'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={key}'
CITIES = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]

# Initialize DB connection
conn = sqlite3.connect('weather_data.db', check_same_thread=False)
cursor = conn.cursor()

# Create a table for storing weather data if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        temp REAL,
        feels_like REAL,
        main TEXT,
        humidity REAL,
        wind_speed REAL,
        timestamp DATETIME
    )
''')
conn.commit()

# Function to convert Kelvin to Celsius
def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

# Function to fetch weather data from OpenWeatherMap API
def get_weather(city):
    url = BASE_URL.format(city=city, key=API_KEY)
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200:
        weather = {
            'city': city,
            'temp': kelvin_to_celsius(data['main']['temp']),
            'feels_like': kelvin_to_celsius(data['main']['feels_like']),
            'main': data['weather'][0]['main'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'timestamp': datetime.fromtimestamp(data['dt'])
        }
        return weather
    else:
        st.error(f"Failed to retrieve data for {city}: {data['message']}")
        return None

# Store weather data in the database
def store_weather_data(weather):
    cursor.execute('''
        INSERT INTO weather (city, temp, feels_like, main, humidity, wind_speed, timestamp) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (weather['city'], weather['temp'], weather['feels_like'], weather['main'], 
          weather['humidity'], weather['wind_speed'], weather['timestamp']))
    conn.commit()

# Fetch and process data every 5 minutes
def fetch_weather_data():
    for city in CITIES:
        weather = get_weather(city)
        if weather:
            store_weather_data(weather)
        time.sleep(1)  # Prevent hitting rate limits

# Roll up daily aggregates
def get_daily_summary():
    query = '''
        SELECT city, date(timestamp) as date, 
               AVG(temp) as avg_temp, MAX(temp) as max_temp, MIN(temp) as min_temp,
               AVG(humidity) as avg_humidity, AVG(wind_speed) as avg_wind_speed,
               main, COUNT(main) as cnt 
        FROM weather
        GROUP BY city, date, main 
        ORDER BY date DESC, cnt DESC
    '''
    df = pd.read_sql_query(query, conn)
    return df

# Function to visualize daily summaries in Streamlit
def show_weather_summary():
    st.title("Daily Weather Summary")
    
    # Fetch summary data
    df = get_daily_summary()
    
    # Display in Streamlit
    st.write("Weather Summary by City")
    st.dataframe(df)

# Threshold alerting system
def check_alerts():
    threshold_temp = st.number_input("Set Temperature Threshold (°C)", value=35)
    
    st.write(f"Checking alerts for temperatures exceeding {threshold_temp}°C.")
    
    query = '''
        SELECT city, temp, timestamp 
        FROM weather 
        WHERE temp > ? 
        ORDER BY timestamp DESC
    '''
    df = pd.read_sql_query(query, conn, params=(threshold_temp,))
    
    if not df.empty:
        st.write(f"Temperature exceeded the threshold in the following cities:")
        st.dataframe(df)
    else:
        st.write("No alerts triggered.")

# Function to fetch weather forecast from OpenWeatherMap API
def get_weather_forecast(city):
    url = FORECAST_URL.format(city=city, key=API_KEY)
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        forecasts = []
        for forecast in data['list']:
            forecasts.append({
                'city': city,
                'temp': kelvin_to_celsius(forecast['main']['temp']),
                'feels_like': kelvin_to_celsius(forecast['main']['feels_like']),
                'humidity': forecast['main']['humidity'],
                'wind_speed': forecast['wind']['speed'],
                'main': forecast['weather'][0]['main'],
                'timestamp': datetime.fromtimestamp(forecast['dt'])
            })
        return forecasts
    else:
        st.error(f"Failed to retrieve forecast data for {city}: {data['message']}")
        return None

# Store forecast data in a separate table
def store_forecast_data(forecasts):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS forecast (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            temp REAL,
            feels_like REAL,
            humidity REAL,
            wind_speed REAL,
            main TEXT,
            timestamp DATETIME
        )
    ''')
    conn.commit()

    for forecast in forecasts:
        cursor.execute('''
            INSERT INTO forecast (city, temp, feels_like, humidity, wind_speed, main, timestamp) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (forecast['city'], forecast['temp'], forecast['feels_like'], 
              forecast['humidity'], forecast['wind_speed'], forecast['main'], forecast['timestamp']))
    conn.commit()

# Function to display weather forecast
def show_weather_forecast():
    st.title("Weather Forecast")
    
    # Choose a city for forecast
    city = st.selectbox("Select a city", CITIES)
    
    # Fetch and display forecast data
    forecasts = get_weather_forecast(city)
    if forecasts:
        forecast_df = pd.DataFrame(forecasts)
        st.write(f"Weather forecast for {city}")
        st.dataframe(forecast_df)

# Main Streamlit app
def main():
    add_custom_css()  # Apply CSS styling

    st.sidebar.title("Weather Monitoring System")
    choice = st.sidebar.radio("Navigation", ["Home", "Weather Summary", "Set Alerts", "Weather Forecast"])
    
    if choice == "Home":
        st.write("Fetching real-time weather data...")
        fetch_weather_data()
        st.write("Weather data fetched successfully.")
    
    elif choice == "Weather Summary":
        show_weather_summary()
    
    elif choice == "Set Alerts":
        check_alerts()
    
    elif choice == "Weather Forecast":
        show_weather_forecast()

if __name__ == "__main__":
    main()
