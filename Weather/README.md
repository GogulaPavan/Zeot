# Weather Monitoring System

This project is a weather monitoring system built with Streamlit and OpenWeatherMap API. It fetches real-time weather data for multiple cities, stores it in a SQLite database, and allows users to view daily weather summaries, set alerts for high temperatures, and see future weather forecasts.

## Table of Contents
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Design Choices](#design-choices)
- [Dependencies](#dependencies)
- [Docker Setup](#docker-setup)

## Features

- **Real-Time Weather Fetching:** Fetches current temperature, humidity, and wind speed for multiple cities.
- **Weather Summary:** Provides daily summary with averages, maximum, and minimum values.
- **Temperature Alerts:** Allows users to set a threshold for alerts when temperature exceeds a certain value.
- **Weather Forecast:** Retrieves and displays future weather predictions for selected cities.
- **Custom UI:** A colorful and responsive user interface built using Streamlit.

## Technology Stack
- **Frontend/UI:** Streamlit
- **Backend:** Python (with SQLite for database)
- **API:** OpenWeatherMap API
- **Database:** SQLite (local database)
  
## Installation

### Step 1: Clone the Repository
Clone the GitHub repository to your local machine.
```bash
git clone https://github.com/GogulaPavan/Weather-Monitoring-System.git
cd Weather-Monitoring-System
