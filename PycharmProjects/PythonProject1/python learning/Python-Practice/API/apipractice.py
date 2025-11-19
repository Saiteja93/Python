import requests
import json

response = requests.get("https://jsonplaceholder.typicode.com/todos/1")
response.raise_for_status()
web_site = response.json()
print(web_site)