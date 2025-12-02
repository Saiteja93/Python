import requests

USERNAME = "ramu123"
TOKEN = "shdugfieyfuegdfuedeueufg"
pixela_endpoint = "https://pixe.la/v1/users"
user_params = {
    "token" : TOKEN,
    "username" : USERNAME,
    "agreeTermsOfService" : "yes",
    "notMinor" : "yes",

}
#response = requests.post(url=pixela_endpoint, json=user_params)
#print(response.text)

graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

graphs_config = {
    "id" : "graph9393",
    "name" : "cycling graph",
    "unit" : "km",
    "type" : "float",
    "color" : "ajisai",


}

headers = {
    "X-USER-TOKEN" : TOKEN
}

response = requests.post(url=graph_endpoint, json=graphs_config, headers= headers)
print(response.text)



