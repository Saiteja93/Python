import requests

blogs_url = requests.get("https://jsonplaceholder.typicode.com/posts")
data = blogs_url.json()

user_data_1 = [post for post in data if post['userId'] == 1]

for post in user_data_1:
    print(f"ID: {post['id']}")
    print(f"Title: {post['title']}")
    print(f"Body: {post['body']} \n")



