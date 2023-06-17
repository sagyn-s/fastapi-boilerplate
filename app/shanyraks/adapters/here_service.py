import requests


class HereService:
    def __init__(self, api_key):
        self.api_key = api_key
    
    def get_coordinates(self, address):
        url = f"https://geocode.search.hereapi.com/v1/geocode?q={address}&apiKey={self.api_key}"
        response = requests.get(url)
        json = response.json()
        if not json["items"]:
            return {
                "latitude": 0,
                "longitude": 0
            }
        return {
            "latitude": json["items"][0]["position"]["lat"],
            "longitude": json["items"][0]["position"]["lng"]
        }