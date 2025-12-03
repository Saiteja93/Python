import requests
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"
TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"

class FlightSearch:
    def __init__(self):
        self._api_key = os.environ["AMADEUS_API_KEY"]
        self._api_secret = os.environ["AMADEUS_SECRET"]
        self._token = self.get_new_token()

    def get_new_token(self):
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret
        }
        response = requests.post(url=TOKEN_ENDPOINT, headers=header, data=body)
        print(f"your token is {response.json()['access_token']}")
        print(f"your token is expires in {response.json()['expires']} seconds")
        return response.json()['access_token']



    def get_destination_code(self, city_name):
        print(f"using this token to get destination{self._token}")
        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "keyword": city_name,
            "max": "2",
            "include": "AIRPORTS",
        }
        response = requests.get(
            url=IATA_ENDPOINT,
            headers=headers,
            params=query
            )


        print(f"Status code {response.status_code}. Airport IATA: {response.text}")
        try:
            code = response.jspn()["data"][0]["iatacode"]
        except IndexError:
            print(f"Index error: No Airport code found for {city_name}")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city_name}")
            return "Not Found"
        return code
    #This class is responsible for talking to the Flight Search API.
    pass