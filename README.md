# 🌦️ Weather BI Dashboard

## Overview

This project is a **Weather BI Dashboard** built using **Streamlit** and **WeatherAPI**. It allows users to view the current weather, a 7-day weather forecast, and additional weather metrics such as humidity, wind speed, UV index, and more. The dashboard also provides a visual map of the location and displays animated icons based on weather conditions.

## Features

- **Current Weather Data**: View real-time weather data including temperature, humidity, wind speed, etc.
- **7-Day Forecast**: See the forecast for the next 7 days.
- **Weather Data Visualizations**: Interactive charts for temperature trends and additional weather metrics.
- **Dynamic Location Selection**: Select different countries and cities for weather data.
- **Animated Weather Icons**: The app uses animated icons based on weather conditions (e.g., animated clouds, sun, rain).

## Dashboard Preview

![Dashboard Screenshot](path/to/your/screenshot1.png)  
*Dashboard Overview*

![Temperature Trend Chart](path/to/your/screenshot2.png)  
*Temperature Trend for the Next 7 Days*

![Weather Metrics Chart](path/to/your/screenshot3.png)  
*Weather Metrics (Cloud, UV, Dewpoint, etc.)*

## Requirements

- Python 3.x
- Streamlit
- Requests
- Plotly
- pandas

### To install the required packages, create a virtual environment and install dependencies using:

```bash
pip install -r requirements.txt
```
requirements.txt includes the following dependencies:
```bash
streamlit
requests
plotly
pandas
```
How to Run the App
Clone the repository:

```bash

git clone https://github.com/dhananjayaDev/streamlit-weather-dashboard.git
cd streamlit-weather-dashboard
```
Create and activate a virtual environment:

For Windows:

```bash
python -m venv venv
.\venv\Scripts\activate
```
For macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```
Install the required packages:

```bash
pip install -r requirements.txt
```
Run the Streamlit app:

```bash
streamlit run weather_dashboard.py
```
Open the browser and navigate to http://localhost:8501 to view the dashboard.

License
This project is licensed under the MIT License - see the LICENSE file for details.
