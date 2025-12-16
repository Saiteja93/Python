import random
from datetime import datetime
import requests

from flask import Flask, render_template

app = Flask(__name__)
random_number_1 = random.randint(1,10)


year = datetime.now().year

@app.route('/')
def home():
    return render_template("home.html", number = random_number_1, year = year)




@app.route('/blogs')
def blogs():
    blogs_url = requests.get("https://jsonplaceholder.typicode.com/posts")
    posts_data = blogs_url.json()

    # Get unique userIds
    user_ids = sorted({post['userId'] for post in posts_data})

    return render_template('blogs.html', posts_data=posts_data, user_ids=user_ids)




@app.route('/blogs/<int:user_id>')
def blogs_by_user(user_id):

    blogs_url = requests.get("https://jsonplaceholder.typicode.com/posts")
    posts_data = blogs_url.json()
    user_data_index = [post for post in posts_data if post['userId'] == user_id]
    return render_template("blogs_index.html", posts = user_data_index)






if __name__ == "__main__":
    app.run(debug=True)