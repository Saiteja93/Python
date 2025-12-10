import requests

gender_url= requests.get("https://api.genderize.io?name=peter")
data = gender_url.json()
print(data)

age_url = requests.get("https://api.agify.io?name=michael")
age_data = age_url.json()
print(age_data["age"])

url = requests.get("https://www.npoint.io/docs/c790b4d5cab58020d391")
print("STATUS:", url.status_code)
all_blogs = url.json()

print(all_blogs)
