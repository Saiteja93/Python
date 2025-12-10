import requests
import json
from datetime import datetime

from boto3.resources.model import Parameter

#response = requests.get("https://jsonplaceholder.typicode.com/todos/1")
#response.raise_for_status()
#web_site = response.json()
#print(web_site)
#MY_LAT = 51.507351
#MY_LONG = -0.127758

MY_LAT = 37.356256
MY_LONG = -482.028111



parameters = {
    "lat" : MY_LAT,
    "lng" : MY_LONG,
    "formatted" :0
}

response = requests.get("https://api.sunrise-sunset.org/json", params = parameters)
response.raise_for_status()
data = response.json()
print(data)
sunrise = data["results"]["sunrise"].split('T')[1]
sunset = data["results"]["sunset"].split('T')[1]

time_now = datetime.now()
print(f"Current time :{time_now}")

print(f"Sunrise ----> {sunrise}")
print(f"Sunset -----> {sunset}")



