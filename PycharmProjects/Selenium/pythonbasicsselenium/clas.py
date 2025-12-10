class BasicCalculator():

    def __init__(self, a, b):
        self.firstnumber = a
        self.secondnumber = b

    def Addition(self):
        return self.firstnumber + self.secondnumber

    def Subtraction(self):
        return self.firstnumber - self.secondnumber

    def Multiplication(self):
        return self.firstnumber * self.secondnumber

    def Divison(self):
        return self.firstnumber / self.secondnumber


obj = BasicCalculator(10, 5)
print(f"Addition: 10 + 5 = {obj.Addition()}")


def GreetUser(username):
    print(f"Hello, {username}! Welcome to the Python course.")


GreetUser("John")



items_in_cart = 0

def  add_to_cart(itemstoadd):
    global items_in_cart



    if items_in_cart + itemstoadd > 5:
        raise Exception ("items should not add more than 5")

    if itemstoadd < 0:
        raise Exception("dont add negative number of items")

    items_in_cart += itemstoadd
    print (f"{itemstoadd} items added. Total in cart: {items_in_cart}")


try:
    add_to_cart(2)
    add_to_cart(-1)

except Exception as e:
    print(e)




