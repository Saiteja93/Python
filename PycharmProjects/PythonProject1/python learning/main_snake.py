import turtle
from turtle import Screen, Turtle
from Snake import Snake
import time



screen = Screen()
screen.setup(600, 600)
screen.bgcolor("black")
screen.title("my snake game")
screen.tracer(0)
snake = Snake()


game_is_on = True
while game_is_on:
    screen.update()
    time.sleep(0.1)

    snake.move()






