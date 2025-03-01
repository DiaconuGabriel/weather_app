import requests

class LocationAPI:
    def __init__(self, location_api_key):
        self.base_url = 'https://api.geoapify.com/v1/geocode/search?city='
        self.country = "&country=România"
        self.format = "&format=json"
        self.type = "&type=city"
        self.limit = "&limit=1"
        self.apikey = f"&apiKey={location_api_key}"

    def get_location(self, city):
        url = f"{self.base_url+city+self.country+self.type+self.format+self.limit+self.apikey}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            locations = []
            data = response.json()
            if "results" not in data or not data["results"]:
                print("No results found")
                raise Exception("Nu exita date")
            
            locations = {"latitude": data["results"][0]["lat"], "longitude":data["results"][0]["lon"]} 
            return locations
        except requests.exceptions.HTTPError as http_err:
            raise Exception("Ai failed to responde")
        except Exception as err:
            print(f"Other error occurred: {err}")

