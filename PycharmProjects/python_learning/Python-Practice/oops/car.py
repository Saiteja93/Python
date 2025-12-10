class Car:

    def __init__(self, model, year):
        self.model = model
        self.year = year
    
    def car_info(self):
        print(f"\nYou choose a car model {self.model.title()} and car manufacture in {self.year} ")
        
      

class Electric_car(Car):
        
        def __init__(self,model,valid_models,year, reg_number):
            super().__init__(model, year)
            self.valid_models = valid_models
            self.reg_number = reg_number

        def Service_vehicle(self, reg_number):
            if self.model in self.valid_models:
                print(f"Your car model is going to start service. we will update once service is completed.\n Car details: \n model : {self.model}\n year : {self.year}\n")
            else:
                print("please choose a valid model in electric vehicle to start service")
                 
        
        def Purchase(self):
             if self.model in self.valid_models:
                  print(f"\nYou purchased a electric vehicle\nmodel : {self.model.title()} \nyear: {self.year} \nCharging : 100 percentage \nReg_number: {self.reg_number}")
                  return True
             
        def Start(self):
            if self.model in self.valid_models:
                self.car_info()
                print(f"{self.model.title()} is an Electric Car ⚡ — battery powered.\n")
                return True
            else:
                print("Please choose a valid model in electric vehicles")
                return False
            
       

            
class Gas_car(Car):
        
        def __init__(self,model, valid_models,year, reg_number):
            super().__init__(model,year)
            self.valid_models = valid_models
            self.reg_number = reg_number
        
        def Service_vehicle(self, reg_number):
            if self.model in self.valid_models:
                print(f"Your car model is going to start service. we will update once service is completed.\nCar details: \n Car reg number : {self.reg_number}\n model : {self.model}\n year : {self.year}")
            else:
                print("please choose a valid model in gas vehicle to start service")
                 
                 
             

        def Purchase(self):
            if self.model in self.valid_models:
                print(f"\nYou purchased a gas vehicle\nmodel : {self.model.title()} \nYear : {self.year} \nMiles = 0 \nFuel tank = 360miles \nRegistration : {self.reg_number}")
                return True
             

        def Start(self):
            if self.model in self.valid_models:
                self.car_info()
                print(f"{self.model.title()} is a Gas Car ⛽ — runs on petrol.\n")
                return True
            else:
                print("please choose a valid model in gas vehicle")
                return False
                
               
                
            

       
            
         
        
        



           
        
    


   










        