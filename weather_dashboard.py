import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ========== SETTINGS ==========
API_KEY = "ee4046c156c4403db3f172241250107"  # Replace with your valid API key

country_city_map = {
    "Sri Lanka": ["Colombo", "Kandy", "Galle", "Jaffna"],
    "India": ["Delhi", "Mumbai", "Bangalore", "Kolkata"],
    "USA": ["New York", "Los Angeles", "Chicago", "Houston"],
    "UK": ["London", "Manchester", "Bristol", "Edinburgh"]
}

st.set_page_config(layout="wide", page_title="🌍 Weather BI Dashboard")
st.title("🌦️ Global Weather BI Dashboard")

# ========== Sidebar ==========
with st.sidebar:
    st.markdown("### ☁️ Choose Location")
    country = st.selectbox("🌐 Country", sorted(country_city_map.keys()))
    city = st.selectbox("🏙️ City", sorted(country_city_map[country]))

# ========== Fetch Weather Data ==========
current_url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
forecast_url = f"https://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=7"

try:
    cur_res = requests.get(current_url, timeout=10)
    for_res = requests.get(forecast_url, timeout=10)

    if cur_res.status_code == 200 and for_res.status_code == 200:
        current_data = cur_res.json()
        forecast_data = for_res.json()

        location = current_data["location"]
        current = current_data["current"]
        condition = current["condition"]
        forecast_days = forecast_data["forecast"]["forecastday"]

        # ========== Choose Icon by Condition ==========
        condition_text = condition["text"].lower()
        icon_url = "https://img.icons8.com/ios-filled/50/ffffff/cloud.png"  # Default cloudy

        if "rain" in condition_text:
            icon_url = "https://img.icons8.com/ios-filled/50/ffffff/rain.png"
        elif "sun" in condition_text or "clear" in condition_text:
            icon_url = "https://img.icons8.com/ios-filled/50/ffffff/sun.png"

        # ========== Layout: Icon + Weather Info ==========
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(icon_url, width=100)
        with col2:
            st.markdown(f"### 🌤️ {condition['text']}")
            st.markdown(f"**📍 {location['name']}, {location['region']}**")
            st.markdown(f"**🌍 {location['country']}**")
            st.markdown(f"**🕓 Local Time:** {location['localtime']}")
            st.markdown(f"**📌 Lat, Lon:** {location['lat']}, {location['lon']}")

        # ========== Metrics ==========
        metric_cols = st.columns(4)
        metric_cols[0].metric("🌡️ Temp (°C)", current["temp_c"])
        metric_cols[1].metric("🤒 Feels Like", current["feelslike_c"])
        metric_cols[2].metric("💧 Humidity", f"{current['humidity']}%")
        metric_cols[3].metric("🌬️ Wind", f"{current['wind_kph']} kph")

        # ========== Forecast Table ==========
        st.markdown("## 📅 7-Day Forecast")
        forecast_df = pd.DataFrame([{
            "Date": day["date"],
            "Condition": day["day"]["condition"]["text"],
            "Max Temp (°C)": day["day"]["maxtemp_c"],
            "Min Temp (°C)": day["day"]["mintemp_c"],
            "Humidity (%)": day["day"]["avghumidity"],
            "Chance of Rain (%)": day["day"].get("daily_chance_of_rain", 0)
        } for day in forecast_days])
        st.dataframe(forecast_df, use_container_width=True)

        # ========== Line Chart ==========
        st.markdown("### 📈 Temperature Trend")
        fig = px.line(
            forecast_df,
            x="Date",
            y=["Max Temp (°C)", "Min Temp (°C)"],
            markers=True,
            color_discrete_map={"Max Temp (°C)": "#ff6e6e", "Min Temp (°C)": "#1f77b4"},
        )
        fig.update_layout(legend_title_text="Temperature")
        st.plotly_chart(fig, use_container_width=True)

        # ========== Bar Chart ==========
        bar_df = pd.DataFrame({
            "Metric": [
                "Cloud (%)", "UV Index", "Dew Point (°C)",
                "Pressure (mb)", "Precipitation (mm)", "Visibility (km)"
            ],
            "Value": [
                current["cloud"], current["uv"], current["dewpoint_c"],
                current["pressure_mb"], current["precip_mm"], current["vis_km"]
            ]
        })
        st.markdown("### 📊 Atmospheric Metrics")
        fig2 = go.Figure(go.Bar(
            x=bar_df["Value"],
            y=bar_df["Metric"],
            orientation='h',
            marker_color='lightblue'
        ))
        fig2.update_layout(height=350, margin=dict(l=40, r=40, t=40, b=20))
        st.plotly_chart(fig2, use_container_width=True)

        # ========== Map ==========
        st.markdown("### 🗺️ Map Location")
        st.map(pd.DataFrame({"lat": [location["lat"]], "lon": [location["lon"]]}), zoom=5)

    else:
        st.error(f"⚠️ API Error: Status Code {cur_res.status_code} or {for_res.status_code}. Please check the API key or city.")

except requests.exceptions.RequestException as e:
    st.error(f"⚠️ Network Error: {str(e)}. Please check your internet connection.")
except Exception as e:
    st.error(f"⚠️ Unexpected Error: {str(e)}. Please try again later.")