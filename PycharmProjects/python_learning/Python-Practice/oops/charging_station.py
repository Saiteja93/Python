class charging_Station:
    def __init__(self, station_battery = 1000, max_per = 100):
      
        self.station_battery = station_battery
        self.max_per = max_per



    def refill(self, amount):
        self.station_battery += amount
        print(f"♻️ Station refilled by {amount} kW. Total: {self.station_battery} kW.\n")


    
    def charge_car(self, car,current_battery):
        if car.model not in car.valid_models:
            print("Please choose a valid model option")
            return
        if not  (0 <= current_battery <100):
            print("Battery level must be between 0 -100")
            return
        

        needed = 100 - current_battery
        if needed > self.max_per:
            needed = self.max_per

        if needed > self.station_battery:
            needed = self.station_battery

        car.battery_level = current_battery + needed
        if car.battery_level > 100:
            car.battery_level = 100


        self.station_battery -= needed


        print(f"✅ Car {car.reg_number} ({car.model.title()}) charged by {needed}% — Battery now {car.battery_level}%")
        print(f"⚡ Station remaining power: {self.station_battery} kW.\n")



    
            



    

