from flask import Flask
import random
random_number = random.randint(0,9)
print(random_number)

app = Flask(__name__)
@app.route('/')
def home():
    return '''
            <h1 style = "text-align :center">Guess a number between 0 and 9</h1>
            <div style = "text-align:center;">
               <img src = "https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif" width = "600">
            </div>
            '''
@app.route('/<int:guess>')
def guessing_number(guess):
    if random_number == guess:
        return '''
              <h1 style = "color : green;">You found me</h1>
              <img src="https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif">
               '''
    elif random_number < guess:
        return '''
               <h1 style = "color : red;">Too high try again</h1>
              <img src="https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif">
               '''
    else:
        return '''
             <h1 style = "color : blue;">Too low try again</h1>
              <img src="https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif">
               '''




if __name__ == "__main__":
    app.run(debug=True)
