import time


def delay_decorator(function):
    def wraper_function():
        time.sleep(2)
        function()
        function()

    return wraper_function

@delay_decorator
def hello():
    print("hi hello")

def bye():
    print("Bye")

def greet():
    print("how are you")

hello()
greet()
bye()
