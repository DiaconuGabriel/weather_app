import pandas as pd
import openmeteo_requests
import requests
from datetime import datetime

class WeatherAPI:
    def __init__(self, weather_api_key):
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "https://api.open-meteo.com/v1/forecast?"
        self.openmeteo = openmeteo_requests.Client()  
        self.weather_api_key=weather_api_key 
    
    def get_weather(self, lat, lon):
        url = f"{self.base_url}?lat={lat}&lon={lon}&units=metric&appid={self.weather_api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
          
            data = response.json()
            
            weather_info = {
                "city": data["name"],
                "temperature": f'{data["main"]["temp"]}',
                "weather": f'{data["weather"][0]["description"]}',
                "sunrise": f'{datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%h:%m")}',
                "sunset": f'{datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%h:%m")}',
                "temperature_min": f'{data["main"]["temp_min"]}',
                "temperature_max": f'{data["main"]["temp_max"]}',
                "humidity": f'{data["main"]["humidity"]}',
                "wind_speed": f'{data["wind"]["speed"]}',
                "feels_like": f'{data["main"]["feels_like"]}',
                "clouds": f'{data["clouds"]["all"]}',
                "presure": f'{data["main"]["pressure"]}',
                "date": data["dt"]
            }
            return weather_info
        except requests.exceptions.HTTPError as http_err:
            raise Exception("Failed to get weather data!")
        except Exception as err:
            print(f"Other error occurred: {err}")
    
    def get_forecast(self, lat, lon, date):
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": ["temperature_2m", "precipitation", "weather_code"],
            "timezone": "Europe/Berlin",
            "forecast_days": 3
        }
        date_time = pd.to_datetime(date, unit = "s", utc = True)
        date_time_local = date_time.tz_convert('Europe/Bucharest')
        date_flored = date_time_local.floor('H')

        try:
            responses = self.openmeteo.weather_api(self.forecast_url, params=params)
            response = responses[0] 

            hourly = response.Hourly()
            hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
            hourly_precipitation = hourly.Variables(1).ValuesAsNumpy()
            hourly_weather_code =  hourly.Variables(2).ValuesAsNumpy()

            hourly_data = {"date": pd.date_range(
                start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
                end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
                freq = pd.Timedelta(seconds = hourly.Interval()),
                inclusive = "left"
            )}

            hourly_data["temperature_2m"] = hourly_temperature_2m.round(0).astype(int)
            hourly_data["precipitation"] = hourly_precipitation.round(0).astype(int)
            hourly_data["weather_code"] = hourly_weather_code.round(0).astype(int)

            hourly_dataframe = pd.DataFrame(data = hourly_data)
            hourly_dataframe['date'] = pd.to_datetime(hourly_dataframe['date']).dt.tz_convert('Europe/Bucharest')
            filtered_df = hourly_dataframe[hourly_dataframe['date'] >= date_flored]

            filtered_df_head_12 = filtered_df.head(12)
        
            return filtered_df_head_12

        except requests.exceptions.HTTPError as http_err:
            raise Exception("Failed to get forecast data!")
        except Exception as err:
            print(f"Other error occurred: {err}")