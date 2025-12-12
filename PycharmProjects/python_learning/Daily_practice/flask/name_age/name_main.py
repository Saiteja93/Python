import random
from datetime import datetime
import requests

from flask import Flask, render_template

app = Flask(__name__)
random_number_1 = random.randint(1,10)

response = requests.get("https://api.agify.io/?name=michael")
gender_response = response.json()
Gender = gender_response['age']
print(Gender)





year = datetime.now().year

@app.route('/')
def home():
    return render_template("home.html", number = random_number_1, year = year)
@app.route('/<name>')
def guess_age(name):
    response = requests.get(f"https://api.agify.io/?name={name}")
    age_data = response.json()
    age = age_data['age']
    gender_response = requests.get(f"https://api.genderize.io?name={name}")
    gender_data = gender_response.json()
    gender = gender_data['gender']

    return render_template("index.html", name = name, gender = gender, age = age)

@app.route('/blogs')
def blog():
    blogs_url = requests.get("https://jsonplaceholder.typicode.com/posts")
    posts_data = blogs_url.json()

    # user_data_1 = [post for post in data if post['userId'] == 1]
    #
    # for post in user_data_1:
    #     print(f"ID: {post['id']}")
    #     print(f"Title: {post['title']}")
    #     print(f"Body: {post['body']} \n")

    return render_template("blogs.html", posts_data = posts_data)




if __name__ == "__main__":
    app.run(debug=True)