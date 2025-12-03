import requests
import os
from dotenv import load_dotenv
from datetime import datetime

GENDER = "male"
WEIGHT =  70
HEIGHT =  175
AGE = 32


load_dotenv()
api_key = os.getenv("API_KEY")
app_id = os.getenv("APP_ID")

Authentication = {

    "x-app-id": app_id,
    "x-app-key": api_key,
}


endpoint = "https://app.100daysofpython.dev/v1/nutrition/natural/exercise"
sheet_endpoint = os.environ["SHEET_ENDPOINT"]
exercise_text = input("Tell which exercise you done today: ")

request_body = {
    "query" : exercise_text,
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "age": AGE,
    "gender": GENDER,

}

response = requests.post(url=endpoint, json=request_body, headers= Authentication)

result = response.json()
print(result)

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

bearer_headers = {
    "Authorization": f"Bearer {os.environ['TOKEN']}"
}

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(sheet_endpoint, json=sheet_inputs, headers=bearer_headers)

    print(sheet_response.text)

