import time
import streamlit as st
import pandas as pd
from pandas import Timestamp
import other.fundal as fundal 
from Api.locationapi import LocationAPI
from Api.weatherapi import WeatherAPI
from Api.airqualityapi import AirQualityAPI
from Api.aiapi import AIAPI
from other.weather_codes import weather_codes
from other.orase import cities
import streamlit.components.v1 as components

oras = "NA"; temperatura = "NA"; temperatura_min = "NA"; temperatura_max = "NA"; vreme = "NA"; umidiate ="NA"; vit_vant = "NA"; sunrise = "NA"; sunset = "NA"; se_simte = "NA"; nori = "NA"; presiune = "NA";
co = "NA"; no2 = "NA"; o3 ="NA"; pm10 ="NA"; pm25 = "NA"; so2 = "NA"; air_quality_index = "NA"
data = [("🌥️", "NA", "NA", "NA") for _ in range(12)]
text = ""
words = text.split()
current_text = ""

def modify_data(weather, air_quality_data, forecast):
    global temperatura, temperatura_min, temperatura_max, vreme, umidiate, vit_vant, sunrise, sunset, se_simte, nori, presiune
    global co, no2, o3, pm10, pm25, so2, air_quality_index

    temperatura = weather['temperature']
    temperatura_min = weather['temperature_min']
    temperatura_max = weather['temperature_max']
    vreme = weather['weather']
    umidiate = weather['humidity']
    vit_vant = weather['wind_speed']
    sunrise = weather['sunrise']
    sunset = weather['sunset']
    se_simte = weather['feels_like']
    nori = weather['clouds']
    presiune = weather['presure']
    
    no2 = air_quality_data['NO2']
    co = air_quality_data['CO']
    o3 = air_quality_data['O3']
    pm10 = air_quality_data['PM10']
    pm25 = air_quality_data['PM2.5']
    so2 = air_quality_data['SO2']
    air_quality_index = air_quality_data['overall_aqi']

    global data

    forecast_df = pd.DataFrame(forecast)

    data = [
        ((weather_codes.get(row['weather_code'])[0]), row['temperature_2m'], row['date'], (weather_codes.get(row['weather_code'])[1]))
        for _, row in forecast_df.iterrows() 
    ]

# Configurare pagină
st.set_page_config(layout="wide",page_icon="🌥️")

with open("style/style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

if "prompt" not in st.session_state:
    st.session_state.prompt = " "

fundal.set_png_as_page_bg("images/image.png")

with st.container():
    st.markdown('<div class="title">🌥️ Weather & Air Quality App</div>', unsafe_allow_html=True)
    col_hide_1, col_data, col_air_q, col_hide_2= st.columns([0.1,1,1,0.1], border=True)

col_hide_1.markdown('<div class="col_hide_1"></div>', unsafe_allow_html=True)
col_hide_2.markdown('<div class="col_hide_2"></div>', unsafe_allow_html=True)

with col_data:
    st.markdown('<div class="col_data"></div>', unsafe_allow_html=True)
    with st.container():
        col_select_city, col4 = st.columns(2, border=True)
        with col_select_city:
            st.markdown('<div class="select_city"></div>', unsafe_allow_html=True)
            with st.container():
                try:
                    selected_city = st.selectbox("Select city", cities, index=None)

                    placeholder = st.empty()
                    prompt = placeholder.text_input("Describe yourself",value = st.session_state.prompt)
                    if st.button("Show data"):
                        oras = selected_city
                        api_client_location = LocationAPI(st.secrets["location_api_key"])
                        location = api_client_location.get_location(oras)
                        api_client_weather = WeatherAPI(st.secrets["weather_api_key"])
                        weather = api_client_weather.get_weather(location['latitude'],location['longitude'])
                        forecast = api_client_weather.get_forecast(location['latitude'],location['longitude'],weather['date'])
                        air_quality = AirQualityAPI(st.secrets["air_quality_api_key"])
                        air_quality_data = air_quality.get_air_quality(location['latitude'],location['longitude'])
                        ai = AIAPI(st.secrets["ai_api_key"])
                        ai_response = ai.get_ai_advice(prompt,weather,air_quality_data)
                        print(ai_response)
                        modify_data(weather, air_quality_data, forecast)
                        text = ai_response
                        words = text.split()
                        st.session_state.prompt = " "
                except Exception as e:
                    print(e)
                    oras = "NA"; temperatura = "NA"; temperatura_min = "NA"; temperatura_max = "NA"; vreme = "NA"; umidiate ="NA"; vit_vant = "NA"; sunrise = "NA"; sunset = "NA"; se_simte = "NA"; nori = "NA"; presiune = "NA";
                    co = "NA"; no2 = "NA"; o3 ="NA"; pm10 ="NA"; pm25 = "NA"; so2 = "NA"; air_quality_index = "NA"
                    text = f'{e}'
                    words = text.split()    
                
        col4.markdown('<div class="col4"></div>', unsafe_allow_html=True)
        col4.write('📍' + oras); col4.write('🌡️ ' + temperatura+ " °C"); col4.write('Weather: ' + vreme); col4.write("☀️: "+sunrise); col4.write("🔴: "+sunset)

        col_min_max_temp, col_humidity, col_wind_speed = st.columns(3, border=True)

        with col_min_max_temp:
            st.markdown('<div class="col_min_max_temp"></div>', unsafe_allow_html=True)
            st.write("Min: " + temperatura_min + "°C"); st.write("Max: " + temperatura_max + "°C")
        with col_humidity:
            st.markdown('<div class="col_humidity"></div>', unsafe_allow_html=True)
            st.write("💧 Humidity"); st.write(umidiate+" %")
        with col_wind_speed:
            st.markdown('<div class="col_wind_speed"></div>', unsafe_allow_html=True)
            st.write("💨 Wind Speed"); st.write(vit_vant+ " km/h") 

        col_feels_like, col_cloud_coverage, col_pressure = st.columns(3, border=True)
        with col_feels_like:
            st.markdown('<div class="col_feels_like"></div>', unsafe_allow_html=True)
            st.write("🌡️ Feels Like"); st.write(se_simte+ " °C")
        with col_cloud_coverage:
            st.markdown('<div class="col_cloud_coverage"></div>', unsafe_allow_html=True)
            st.write("☁️ Cloud Coverage"); st.write(nori+" %")
        with col_pressure:
            st.markdown('<div class="col_pressure"></div>', unsafe_allow_html=True)
            st.write("⚖️ Pressure"); st.write(presiune + " hPa")

with col_air_q:
    st.markdown('<div class="col_air_q"></div>', unsafe_allow_html=True)

    co_col, no2_col, o3_col, so2_col = st.columns(4, border=True)
    with co_col :
        st.markdown('<div class="co_col"></div>', unsafe_allow_html=True)
        co_col.write("CO"); co_col.write(co + " µg/m³")
    with no2_col:
        st.markdown('<div class="no2_col"></div>', unsafe_allow_html=True)
        so2_col.write("SO2"); so2_col.write(so2 + " µg/m³")
    with o3_col:
        st.markdown('<div class="o3_col"></div>', unsafe_allow_html=True)
        o3_col.write("O3"); o3_col.write(o3 + " µg/m³")
    with so2_col:
        st.markdown('<div class="so2_col"></div>', unsafe_allow_html=True)
        no2_col.write("NO2"); no2_col.write(no2 + " µg/m³")

    pm10_col, pm25_col, aqi_col = st.columns(3, border=True)
    with pm10_col:
        st.markdown('<div class="pm10_col"></div>', unsafe_allow_html=True) 
        pm10_col.write("PM10"); pm10_col.write(pm10 + " µg/m³")
    with pm25_col:
        st.markdown('<div class="pm25_col"></div>', unsafe_allow_html=True)
        pm25_col.write("PM25"); pm25_col.write(pm25 + " µg/m³")
  
    aqi_col.markdown('<div class="aqi_col"></div>', unsafe_allow_html=True)
    aqi_col.write("Air quality index"); aqi_col.write(air_quality_index)

    with st.container():
        st.markdown('<div class="title_ai">🔍 AI Recommendation:</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown(f'<div class="text_ai">{text}</div>', unsafe_allow_html=True)
        # placeholder = st.empty()
        # for word in words:
        #     current_text += " " + word if current_text else word 
        #     placeholder.text(current_text)  
        #     time.sleep(0.035)

col_hide_3, col_4, col_hide_5 = st.columns([0.05,1,0.05])

col_hide_3.markdown('<div class="col_hide_3"></div>', unsafe_allow_html=True)
col_hide_5.markdown('<div class="col_hide_5"></div>', unsafe_allow_html=True)

with col_4:
    with st.container():
        st.markdown('<div class="temperatures_for_the_day">📈 Temperatures for the day</div>', unsafe_allow_html=True)
        columns1 = st.columns(12, border=True)

        for idx, (weather, temp, time, about) in enumerate(data):
            columns1[idx].markdown(f'<div class="forecast_{idx}">{weather}</div>', unsafe_allow_html=True)
            # columns1[idx].write(f'# {weather}')  
            columns1[idx].write(f'{temp}' + " °C")    
            columns1[idx].write(f'{time.strftime("%H:%M")}' if isinstance(time, Timestamp) else time)
            columns1[idx].write(about)
