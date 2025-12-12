from flask import Flask
import random

app = Flask(__name__)

random_number = random.randint(1, 11)

@app.route('/')
def home():
    return """
    <div style="text-align:center;">
        <h1>Guess the number!</h1>
        <p>Choose a number between 1 and 10</p>
        <img src="https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif" height="600"/>
    </div>
    """

@app.route('/<int:num>')
def guessing_number(num):
    if num == random_number:
        return """
        <div style="text-align:center;">
            <h1>You found me! 🎉</h1>
            <img src="https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif" height="600"/>
        </div>
        """
    elif num > random_number:
        return """
        <div style="text-align:center;">
            <h1>Too high! Try again ⬇️</h1>
            <img src="https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif" height="600"/>
        </div>
        """
    else:
        return """
        <div style="text-align:center;">
            <h1>Too low! Try again ⬆️</h1>
            <img src="https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif" height="600"/>
        </div>
        """

if __name__ == "__main__":
    app.run(debug=True)
