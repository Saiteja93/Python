

import requests
import random
import json
import string

#base url
base_url = "https://gorest.co.in"
#auth token
auth_token = "Bearer a52db0655a8e96164408b34d7f03e5838de096430a91bb2a00535833beb3ac77"

def random_mail():
    domain_name = "gmail.com"
    email_length = 10
    random_string = ''.join(random.choice(string.ascii_lowercase) for _ in range(email_length))
    email = random_string + "@" + domain_name
    return email

#Get request
def get_request():
    url = base_url + "/public/v2/users"
    headers = {"Authorization" : auth_token}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    json_body = response.json()
    json_str = json.dumps(json_body, indent=4)
    print("json_body_load : ", json_str)



#Post request
def post_request():
    url = base_url + "/public/v2/users"
    print("post url:" + url)
    headers = {"Authorization" : auth_token}
    data = {
        "name": "naveen kumar",
        "email": random_mail(),
        "gender": "male",
        "status": "active"}
    response = requests.post(url, headers=headers, json=data)
    print("status code :", response.status_code)
    assert response.status_code == 201
    json_body = response.json()
    json_str = json.dumps(json_body, indent=4)
    print("json_data:", json_str)
    print("......user is created.......")
    user_id = json_body["id"]
    assert "name" in json_body
    assert json_body["name"] == "naveen kumar"
    return user_id


#Put request
def put_request(update_id):
    url = base_url + f"/public/v2/users/{update_id}"
    print("put url:" + url)
    headers = {"Authorization": auth_token}
    data = {
        "name": "kumari saroja",
        "email": random_mail(),
        "gender": "female",
        "status": "inactive"}
    response = requests.put(url, headers=headers, json=data)
    print(f"Updating {update_id} information")
    print("response:", response.status_code)
    assert response.status_code == 200
    json_body = response.json()
    json_str = json.dumps(json_body, indent=4)
    print(".......user is updated.......")
    print("update records:", json_str)
    assert "name" in json_body
    assert json_body["name"] == "kumari saroja"
    assert json_body["id"] == update_id


#delete request

def delete_request(update_id):
    url = base_url + f"/public/v2/users/{update_id}"
    print("put url:" + url)
    headers = {"Authorization": auth_token}
    response = requests.delete(url, headers=headers)
    print(f"User {update_id} is deleting...")
    assert response.status_code == 204
    print("Response:", response.status_code)
    print("......user deleted......")



get_request()
update_id = post_request()
put_request(update_id)
zdelete_request(update_id)
