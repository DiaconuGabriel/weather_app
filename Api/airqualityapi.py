import requests

class AirQualityAPI:
    def __init__(self, air_quality_api_key):
        self.base_url = 'https://api.api-ninjas.com/v1/airquality?'
        self.air_quality_api_key = air_quality_api_key

    def get_air_quality(self, lat, lon):
        params = {"lat": lat, "lon": lon}
        headers = {"X-Api-Key": f"{self.air_quality_api_key}"}
        
        try:
            response = requests.get(self.base_url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            return {'CO': f'{data["CO"]["concentration"]}', "NO2": f'{data["NO2"]["concentration"]}', "O3": f'{data["O3"]["concentration"]}',
                    'SO2': f'{data["SO2"]["concentration"]}', "PM2.5": f'{data["PM2.5"]["concentration"]}', "PM10": f'{data["PM10"]["concentration"]}',
                    'overall_aqi': f'{data["overall_aqi"]}'} 
        except requests.exceptions.HTTPError as http_err:
            raise Exception("Failed to get air quality data!")
        except Exception as err:
            print(f"Other error occurred: {err}")

