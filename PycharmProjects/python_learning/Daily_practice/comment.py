my_vehicle = {
    "model": "Ford",
    "make": "Explorer",
    "year": 2018,
    "mileage": 40000
}

for x,y in my_vehicle.items():
    print(f"{x} = {y}")

my_vehilce_2 = my_vehicle.copy()
print(my_vehilce_2)

my_vehilce_2['number_of_tires']=4
print(my_vehilce_2)
my_vehilce_2.pop("mileage")
print(my_vehilce_2)