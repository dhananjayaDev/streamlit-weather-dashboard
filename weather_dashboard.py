import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ========== SETTINGS ==========
API_KEY = ""  # Replace with your valid API key

country_city_map = {
    "Sri Lanka": ["Colombo", "Kandy", "Galle", "Jaffna"],
    "India": ["Delhi", "Mumbai", "Bangalore", "Kolkata"],
    "USA": ["New York", "Los Angeles", "Chicago", "Houston"],
    "UK": ["London", "Manchester", "Bristol", "Edinburgh"]
}

# ========== PAGE CONFIG ==========
st.set_page_config(layout="wide", page_title="🌍 Weather Dashboard")

# ========== CUSTOM CSS FOR DARK THEME ==========
st.markdown("""
    <style>
    .main-card {
        background: linear-gradient(135deg, #FF6B6B, #FF8E6B);
        padding: 20px;
        border-radius: 20px;
        color: white;
        margin: 10px 0;
    }
    .dark-card {
        background: #2D2D2D;
        padding: 15px;
        border-radius: 15px;
        color: white;
        margin: 10px 0;
        border: 1px solid #444;
    }
    .metric-card {
        background: #3D3D3D;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin: 5px;
    }
    .forecast-day {
        background: #2D2D2D;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        margin: 5px;
        min-height: 100px;
    }
    .air-quality-circle {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background: conic-gradient(#FF6B6B 0deg 108deg, #333 108deg 360deg);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
    }
    </style>
""", unsafe_allow_html=True)

# ========== SIDEBAR ==========
with st.sidebar:
    st.markdown("### 🌍 Location Settings")
    country = st.selectbox("Country", sorted(country_city_map.keys()))
    city = st.selectbox("City", sorted(country_city_map[country]))
    
    st.markdown("---")
    st.markdown("### 📊 Dashboard Options")
    show_air_quality = st.checkbox("Show Air Quality", value=True)
    show_precipitation = st.checkbox("Show Precipitation Details", value=True)

# ========== FETCH WEATHER DATA ==========
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

        # ========== MAIN WEATHER CARD ==========
        col1, col2 = st.columns([2, 3])
        
        with col1:
            st.markdown(f"""
            <div class="main-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <h4>{location['name']}</h4>
                    <small>Last Updated: {datetime.now().strftime('%H:%M')}</small>
                </div>
                <div style="display: flex; align-items: center; margin: 20px 0;">
                    <div style="font-size: 48px; margin-right: 20px;">☁️</div>
                    <div>
                        <h1 style="margin: 0; font-size: 3rem;">{current['temp_c']} °C</h1>
                        <p style="margin: 0; opacity: 0.9;">{condition['text']}</p>
                    </div>
                </div>
                <div style="display: flex; justify-content: space-around; margin-top: 20px;">
                    <div style="text-align: center;">
                        <div style="background: rgba(255,255,255,0.2); padding: 8px; border-radius: 8px;">
                            <small>{location['name']}</small><br>
                            <strong>{current['temp_c']}°C</strong>
                        </div>
                    </div>
                    <div style="text-align: center;">
                        <div style="background: rgba(255,255,255,0.2); padding: 8px; border-radius: 8px;">
                            <small>Feels Like</small><br>
                            <strong>{current['feelslike_c']}°C</strong>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # 7-Day Forecast
            st.markdown("### 📅 Weekly Forecast")
            forecast_cols = st.columns(7)
            
            for i, day in enumerate(forecast_days):
                date_obj = datetime.strptime(day['date'], '%Y-%m-%d')
                day_name = date_obj.strftime('%A')[:3]  # Mon, Tue, etc.
                
                with forecast_cols[i]:
                    st.markdown(f"""
                    <div class="forecast-day">
                        <strong>{day_name}</strong><br>
                        <div style="font-size: 24px; margin: 5px 0;">☀️</div>
                        <strong>{day['day']['maxtemp_c']}°C</strong><br>
                        <small style="opacity: 0.7;">{day['day']['mintemp_c']}°C</small>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Location Details under Weekly Forecast
            st.markdown(f"""
            <div class="dark-card" style="margin-top: 15px;">
                <h4 style="text-align: center; margin-bottom: 10px;">Location Details</h4>
                <div style="text-align: center;">
                    <strong style="font-size: 18px;">{location['name']}</strong><br>
                    <span>{location['region']}, {location['country']}</span><br>
                    <small style="opacity: 0.7;">Lat: {location['lat']}, Lon: {location['lon']}</small><br>
                    <small style="opacity: 0.7;">Local Time: {location['localtime']}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ========== SECOND ROW: DETAILED METRICS ==========
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            # Humidity and Wind Speed
            st.markdown(f"""
            <div class="dark-card">
                <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
                    <div style="text-align: center;">
                        <h4>💧 Humidity</h4>
                        <h2>{current['humidity']}%</h2>
                    </div>
                    <div style="text-align: center;">
                        <h4>🌬️ Wind Speed</h4>
                        <h2>{current['wind_kph']} Kph</h2>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Visibility and Pressure
            st.markdown(f"""
            <div class="dark-card">
                <div style="display: flex; justify-content: space-between;">
                    <div style="text-align: center;">
                        <h4>👁️ Visibility</h4>
                        <h3>{current['vis_km']} km</h3>
                    </div>
                    <div style="text-align: center;">
                        <h4>🌡️ Pressure</h4>
                        <h3>{current['pressure_mb']} mb</h3>
                    </div>
                </div>
                <div style="margin-top: 15px; text-align: center;">
                    <h4>🌧️ Precipitation</h4>
                    <h3>{current['precip_mm']} mm</h3>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Map under Visibility/Pressure/Precipitation
            # st.markdown(f"""
            # <div class="dark-card" style="margin-top: 15px;">
            #     <h4 style="text-align: center; margin-bottom: 15px;">🗺️ Map View</h4>
            # </div>
            # """, unsafe_allow_html=True)
            
            # Add the actual map
            st.map(pd.DataFrame({
                "lat": [location["lat"]], 
                "lon": [location["lon"]]
            }), zoom=8, height=200)

        with col2:
            if show_air_quality:
                # Air Quality Overview (Mock data since API doesn't provide this)
                st.markdown("""
                <div class="dark-card">
                    <h3 style="text-align: center; margin-bottom: 20px;">Air Quality Overview</h3>
                    <div style="display: flex; justify-content: space-around; align-items: center;">
                        <div style="text-align: center;">
                            <div class="air-quality-circle">
                                <div style="background: #2D2D2D; width: 100px; height: 100px; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                                    <span style="color: #FF6B6B; font-size: 12px;">Unhealthy for</span>
                                    <span style="color: #FF6B6B; font-size: 12px;">Sensitive</span>
                                    <span style="color: white; font-size: 24px; font-weight: bold;">108</span>
                                </div>
                            </div>
                            <p style="margin-top: 10px; font-size: 12px;">Sensitive groups should reduce outdoor time</p>
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                            <div style="text-align: center;">
                                <span style="color: #FFD700;">●</span> <strong>108</strong><br>
                                <small>PM10</small>
                            </div>
                            <div style="text-align: center;">
                                <span style="color: #90EE90;">●</span> <strong>65</strong><br>
                                <small>O3</small>
                            </div>
                            <div style="text-align: center;">
                                <span style="color: #90EE90;">●</span> <strong>17</strong><br>
                                <small>SO2</small>
                            </div>
                            <div style="text-align: center;">
                                <span style="color: #FFD700;">●</span> <strong>66</strong><br>
                                <small>PM2.5</small>
                            </div>
                            <div style="text-align: center;">
                                <span style="color: #FF6B6B;">●</span> <strong>337</strong><br>
                                <small>CO</small>
                            </div>
                            <div style="text-align: center;">
                                <span style="color: #90EE90;">●</span> <strong>17</strong><br>
                                <small>NO2</small>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Temperature Trend under Air Quality
                st.markdown("### Temperature Trend")
                
                # Prepare data for the chart
                chart_data = []
                for day in forecast_days:
                    chart_data.append({
                        'date': day['date'],
                        'temperature': day['day']['avgtemp_c'],
                        'max_temp': day['day']['maxtemp_c'],
                        'min_temp': day['day']['mintemp_c']
                    })
                
                chart_df = pd.DataFrame(chart_data)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=chart_df['date'],
                    y=chart_df['temperature'],
                    mode='lines+markers',
                    name='Average Temperature',
                    line=dict(color='#FF6B6B', width=3),
                    marker=dict(size=8, color='#FF6B6B')
                ))
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    height=300,
                    showlegend=False,
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
                    margin=dict(l=40, r=40, t=40, b=40)
                )
                
                st.plotly_chart(fig, use_container_width=True)

        with col3:
            # Sunrise and Sunset
            # Note: You might need to get this from forecast data or astronomy API
            st.markdown(f"""
            <div class="dark-card">
                <h4 style="text-align: center; margin-bottom: 15px;">🌅 Sunrise and Sunset</h4>
                <div style="text-align: center; margin: 20px 0;">
                    <div style="margin: 15px 0;">
                        <span style="font-size: 24px;">🌅</span><br>
                        <strong>Sunrise</strong><br>
                        <span style="font-size: 18px;">05:39 AM</span>
                    </div>
                    <div style="margin: 15px 0;">
                        <span style="font-size: 24px;">🌇</span><br>
                        <strong>Sunset</strong><br>
                        <span style="font-size: 18px;">07:27 PM</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Chances of Rain
            st.markdown("""
            <div class="dark-card">
                <h4 style="text-align: center; margin-bottom: 15px;">🌧️ Chances of Rain</h4>
                <div style="margin: 10px 0;">
            """, unsafe_allow_html=True)
            
            # Create rain chance data for the week
            days = ['Friday', 'Saturday', 'Tuesday', 'Thursday', 'Monday', 'Sunday', 'Wednesday']
            rain_chances = [85, 75, 70, 65, 20, 15, 10]  # Mock data
            
            for day, chance in zip(days, rain_chances):
                st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; align-items: center; margin: 5px 0;">
                        <span>{day}</span>
                        <div style="background: #444; width: 100px; height: 8px; border-radius: 4px; position: relative;">
                            <div style="background: #FF6B6B; width: {chance}%; height: 100%; border-radius: 4px;"></div>
                        </div>
                        <span>{chance}%</span>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)



    else:
        st.error(f"⚠️ API Error: Status Code {cur_res.status_code} or {for_res.status_code}. Please check the API key or city.")

except requests.exceptions.RequestException as e:
    st.error(f"⚠️ Network Error: {str(e)}. Please check your internet connection.")
except Exception as e:
    st.error(f"⚠️ Unexpected Error: {str(e)}. Please try again later.")