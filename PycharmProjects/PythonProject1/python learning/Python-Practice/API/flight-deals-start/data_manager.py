import os
import  requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()
SHEETY_PRICES_ENDPOINT = "MY ENDPOINT"


class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self._user = os.environ["SHETTY_USERNAME"]
        self._passwd = os.environ["SHETTY_PASSWORD"]
        self._authorization = HTTPBasicAuth(self._user, self._passwd)
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=SHEETY_PRICES_ENDPOINT, auth=self._authorization)
        data = response.json()
        self.destination_data = data["Prices"]
        return self.destination_data

    def update_destination_code(self):
        for city in self.destination_data:
            new_data = {
                "price" :{
                    "iatcode" : city["iatcode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_PRICES_ENDPOINT}/{city["ID"]}",
                json=new_data,
                auth=self._authorization
            )
            print(response.text)












    pass