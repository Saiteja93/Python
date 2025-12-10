import requests

api_key = "df3728e1d4f14820f82d27090fd78486"
OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
weather_params = {
    "lat" : 37.356256,
    "lon" : -122.028111,
    "appid" : api_key,
    "cnt" : 6

}

response = requests.get(OWM_ENDPOINT, params=weather_params)
response.raise_for_status()
weather_data = response.json()

weather_rain = False
for hour_data in weather_data["list"]:
    weather_code = hour_data["weather"][0]['id']
    print((weather_code))
    if weather_code < 700:
        weather_rain = True

if weather_rain:
    print("Chance of rain in next 12 hours, Bring your umbrella")


