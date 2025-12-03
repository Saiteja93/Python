import requests
from datetime import datetime

USERNAME = "ramu123"
TOKEN = "shdugfieyfuegdfuedeueufg"
pixela_endpoint = "https://pixe.la/v1/users"
ID = "graph9393"
user_params = {
    "token" : TOKEN,
    "username" : USERNAME,
    "agreeTermsOfService" : "yes",
    "notMinor" : "yes",

}
#response = requests.post(url=pixela_endpoint, json=user_params)
#print(response.text)
today = datetime(year=2025, month=12, day=1)
graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

graphs_config = {
    "id" : ID,
    "name" : "cycling graph",
    "unit" : "km",
    "type" : "float",
    "color" : "ajisai",


}

headers = {
    "X-USER-TOKEN" : TOKEN
}

final_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{ID}"

pixel_data = {
    "date" : today.strftime("%Y%m%d"),
    "quantity" : "9.7",

}

#response = requests.post(url=final_endpoint, json=pixel_data, headers= headers)
#print(response.text)

#PUT_ENDPOINT = f"{pixela_endpoint}/{USERNAME}/graphs/{ID}/{today.strftime('%Y%m$d')}"

#response = requests.put(url=PUT_ENDPOINT, json=pixel_data, headers= headers)
#print(response.text)



