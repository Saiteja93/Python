class Menu_Item:
      def __init__(self, name, water, milk, coffee, cost):
        self.name = name
        self.cost = cost
        self.ingredients = {
            "water": water,
            "milk": milk,
            "coffee": coffee
        }


class Menu:
    def __init__(self):
        self.menu = [
            Menu_Item(name="latte", water=200, milk=150, coffee=24, cost=2.5),
            Menu_Item(name="espresso", water=50, milk=0, coffee=18, cost=1.5),
            Menu_Item(name="cappuccino", water=250, milk=50, coffee=24, cost=3),
        ]

    def get_items(self):

        options = ""
        for item in self.menu:
            options += f"{item.name}/"
        return options
    
    def find_drinks(self, order_item):
        for item in self.menu:
            if item.name == order_item:
                return item
            
        print("Please choose a valid option")
            


        

        
 
       
        