
from turtle import Turtle, Screen
from random import random, randint



screen = Screen()
all_turtles = []
is_game_on = False
screen.setup(500, 400)
user_bet = screen.textinput(title="make your bet", prompt="Which turtle win the race, enter a color: ")
colors = ["Red", "Orange", "yellow", "Green", "blue", "Violet"]
y_positions= [-70, -40, -10, 20, 50, 80]
for turtle_index in range (0,6):
    new_turtle = Turtle(shape="turtle")
    new_turtle.penup()
    new_turtle.color(colors[turtle_index])

    new_turtle.goto(x=-230, y=y_positions[turtle_index])
    all_turtles.append(new_turtle)

if user_bet:
    is_game_on = True

while is_game_on:

    for turtle in all_turtles:
        if turtle.xcor() > 230:
            is_game_on = False
            winning_color = turtle.pencolor()
            if winning_color == user_bet:
                print(f"you have won .The {winning_color} turtle won in race")
            else:
                print(f"your color is lost. {winning_color} won the race ")

        random_distance = randint(0, 10)
        turtle.forward(random_distance)

screen.exitonclick()