

import requests
USERNAME = "ramu123"
TOKEN = "shdugfieyfuegdfuedeueufg"

headers = {
    "X-USER-TOKEN" : TOKEN
}


pixela_endpoint = "https://pixe.la/v1/users"
final_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"
response = requests.get(url=final_endpoint, headers=headers )
print(response.status_code)
print(response.text)
