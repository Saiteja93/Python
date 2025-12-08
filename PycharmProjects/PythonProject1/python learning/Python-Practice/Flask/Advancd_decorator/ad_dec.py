class User:
    def __init__(self,name):
        self.name = name
        self.is_logged_info = False

def decorate(func):
    def wrapper(*args):
        user = args[0]
        if user.is_logged_info == True:
            return func(user)

    return wrapper

@decorate
def my_blog(user):
    print(f"This is {user.name}'s new post")


new_user = User("SAI")
new_user.is_logged_info = True
my_blog(new_user)
