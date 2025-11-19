menu = {
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24
        },
        "cost": 2.5
    },
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18
        },
        "cost": 1.5
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24
        },
        "cost": 3.0
    }
}

profit = 0
resources = {
    "water" : 1000,
    "milk" : 500,
    "coffee" : 400
}

is_on = True

def is_resource_sufficient(order_ingredients):
    is_enough = True
    for item in order_ingredients:
        if order_ingredients[item] >= resources[item]:
            print(f"sorry there is no enough {item}. ")
            is_enough = False
    return is_enough


def process_coin():
    print('Please insert coins')
    total = int(input("how many quartesrs: ")) * 0.25
    total += int(input("how many dimes: ")) * 0.1
    total += int(input("how many nickles: ")) * 0.05
    total += int(input("how many pennies: ")) * 0.01
    return total

def make_coffe(drink_name, order_ingredients):
    for item in order_ingredients:
        resources[item] -= order_ingredients[item]
    print(f"Here is your drink {drink_name} ☕️ enjoy!")


def is_transaction_successful(money_received, drink_cost):
    if money_received >= drink_cost:
        change = round(money_received - drink_cost, 2)
        print(f"Hi this is your remaining change {change}$")
        global profit
        profit += drink_cost
        return True
    else:
        print("Sorry this is not enough money for drink, plese pay remaining amount")
        return False



while is_on:
    customer_choice = input("Enter your chocie(latte/espresso,capuccino) or report: ")
    if customer_choice == "off":
        print("Machine turning off")
        is_on = False
   
    elif customer_choice == "report":
        print(f"water : {resources['water']} ml")
        print(f"milk : {resources['milk']} ml")
        print(f"coffee: {resources['coffee']} g")
        print(f"cost : {profit} $")
        
        
    elif customer_choice in menu:
        drink = menu[customer_choice]
        if is_resource_sufficient(drink["ingredients"]):
            payment =  process_coin()
            if is_transaction_successful(payment, drink['cost']):
                make_coffe(customer_choice, drink["ingredients"])
    else:
        print("Invalid option. Please select coffe in menu list")
        


     

       
