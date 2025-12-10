from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return '<h1 style = "text-align : center">Hello, World!</h1>' \
            '<img src= "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExY3FxbmlteHByZ2Q0YW43bG0yMTU0ZmpsNWl2cWgza2xkNTd2a2R0diZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/8TIbelFjFXjIJ0Zg1l/giphy.gif">'

@app.route("/trump")
def bye():
    return '<h1 style = "text-align : center">I am Trump</h1>' \
           '<p>Hi i am trump, i am going to block all IT workers. i am a business man. i love money.</p>' \
           '<img src = "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExaWE5b2o2ZnNlYmppeHpoOTI4cTcwYjhyd2Y3ZGQ1ZnduMDM3Z2I4ayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/o8gLk4EnYuHVCK7tZg/giphy.gif">'

@app.route("/username/<name>/<int:number>")
def name(name,number):
    return f"Hello {name}. How are you. your age is {number}"

if __name__ == "__main__":
    app.run(debug=True)