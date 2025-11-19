greeting = "welcome to python programming"
print (greeting)

instructor = "Rahul!"
print(greeting+ "," + " "+instructor)





# Create the variables and assign their values
age = 25
height = 5.9
favorite_color = "blue"


# Use the print function to display each variable and its type
print(f"Age: {age} | Type: {type(age)}")
print(f"Height: {height} | Type: {type(height)}")
print(f"Favorite Color: {favorite_color} | Type: {type(favorite_color)}")

print (f"my favourite color is {favorite_color} and my height is {height}")

fruits = ["apple", "banana", "cherry", "date", "elderberry"]

print (f"First fruit: {fruits[0]}")
print (f"Last fruit: {fruits[-1]}")
print (f"Fruits from index 1 to 2: {fruits[1 : 2]}")

car = {
     "make": "Toyota",

    "model": "Camry",

    "year": 2020,

    "color": "Blue"
}

print (f"car model: {car["model"]}")
car["owner"] = "Rahul"

# Print the entire dictionary
print(f"Updated car dictionary: {car}")


greeting = "Hellos"

if greeting == "Hello":
    print ("Hello there!")
    print ("How can I assist you today?")
else:
    print ("Greetins!")

    user = 13

    if 5 > user < 11:
        print("Good Morning")
    elif 12 <= user <= 17:
        print("Good Afternoon")
    elif 18 > user < 21:
        print("Good Evening")
    else:
        print("Good Night")
    print("Greeting code has completed")