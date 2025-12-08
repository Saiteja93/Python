from datetime import datetime

from flask import Flask, render_template
import requests

app = Flask(__name__)

current_year = datetime.now().year
@app.route('/')
def home():
    return render_template("index.html", year = current_year)
@app.route('/guess/<person>')
def person_data(person):
    age_url = f"https://api.agify.io?name={person}"
    age_response = requests.get(age_url)
    age_data = age_response.json()
    person_age = age_data["age"]

    gender_url = f"https://api.genderize.io?name={person}"
    gender_response = requests.get(gender_url)
    gender_data = gender_response.json()
    person_gender = gender_data["gender"]

    return render_template ("guess.html", name=person,age = person_age, gender=person_gender )

@app.route('/blog')
def blog_practice():
    url = "https://www.npoint.io/docs/d5298fc148ea8b729831"
    response = requests.get(url)
    all_blogs = response.json()
    return render_template("blog.html", blogs=all_blogs)



if __name__ == "__main__":
    app.run(debug=True)


