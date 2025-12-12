from tkinter.font import names

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/shiva/<name>')
def shiva(name):
    return render_template("shiva.html", name = name)

@app.route('/parvathi/<name>')
def parvathi(name):
    return render_template("parvathi.html", name=name)


if __name__ == "__main__":
    app.run(debug=True)
