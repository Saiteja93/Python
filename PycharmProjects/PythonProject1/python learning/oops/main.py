import json
import os
from car import Electric_car, Gas_car
from charging_station import charging_Station

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_FILE = os.path.join(BASE_DIR, "models.json")
with open(MODEL_FILE) as f:
    models = json.load(f)

station = charging_Station(station_battery=models['station_battery'], max_per = models['max_per'])
sales_on = True
print("Welcome to Sai teja's Auto Hub")

while sales_on:
    print("\nEnter your options in below menu\n")
    print("1 Purchase a new vehicle")
    print("2 Service your electric or gas vehicle")
    print("3 Charge your electric vehicle")
    print("4 Check / Refill charging station")
    print("5 Quit\n")
    choose = input("Enter your selection 1-5: ").strip()



    if choose == '5':
        print("Thank you for visiting Auto Hub , have a great day")
        sales_on = False
    elif choose == '1':
        car_type = input("Enter your car type Electric or Gas: ").lower()
        if car_type in ["electric", "gas"]:
            model = input("Enter your vehicle model: ").lower()
            year = int(input("Enter year of manufacture you want: "))
            valid_models = models[car_type]
            if car_type == 'electric':
                car = Electric_car(model, valid_models,year, reg_number='temporary')
            else:
                car = Gas_car(model, valid_models,year, reg_number= 'temporary')

        is_valid = car.Start()
        if is_valid:
            option = input("Enter your option to purchase of car  yes or no: ").lower()
            if option == 'yes':
               car.Purchase()
            elif option == 'no':
               print("Thank you for checking model details")
               break
            else:
               print("Choose yes or no option")
           
       
    elif choose == '2':
        car_type = input("Enter your car type Electric or Gas: ").lower()
        if car_type in ["electric", "gas"]:
            model = input("Enter your vehicle model: ").lower()
            year = int(input("Enter year of purchase of your car: "))
            reg_number = input("Enter your vehicle register number: ")
            valid_models = models[car_type]
            if car_type == 'electric':
                car = Electric_car(model, valid_models,year,reg_number)
            else:
                car = Gas_car(model, valid_models,year,reg_number)
        car.Service_vehicle(reg_number)

    elif choose == "3":
        model = input("Enter your car model: ").lower()
        reg_number = input("Enter your registration number: ").upper()  # Charge Electric Vehicle
        car = Electric_car(
        model=model,
        valid_models=models['electric'],
        year=2024,          # default or user-specified
        reg_number=reg_number)
        # Create Electric_car object
   
    # Check if model is valid
        if car.Start(): 
             # returns True only if valid model
            try:
                current_battery = int(input("Enter your battery percentage (0-99): "))
                station.charge_car(car, current_battery)
            except ValueError:
               print("❌ Invalid input. Please enter a number between 0–99.\n")
    
          

    elif choose == '4':  # Station info / refill
        print(f"🔋 Charging station has {station.station_battery} kW remaining.")
        refill = input("Do you want to refill the station? (yes/no): ").lower()
        if refill == 'yes':
            try:
                amount = int(input("Enter refill amount (kW): "))
                station.refill(amount)
            except ValueError:
                print("❌ Invalid input.\n")


        
        
    else:
        print("please select a valid option or quit")


   
