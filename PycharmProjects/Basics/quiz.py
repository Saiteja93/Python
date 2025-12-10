print ("Hey hi welcome, do you wanna play quiz!")

playing = input("Are you ready? ")
if playing != "yes":
   quit ()
print ( "okay i am excited lets play! :) ")

score = 0

playing = input("what does CPU stands for? ")
if playing.lower() == "central processing unit":
   print ("Great it is correct answer, you are going to second question ")
   score += 1
   
else :
   print ("sorry it is incorrect answer")

playing = input("what does GPU stands for? ")
if playing.lower() == "graphics processing unit":
   print ("Great it is correct answer, you are going to third question ")
   score += 1
else: 
   print ("sorry it is incorrect answer")

playing = input("what does RAM stands for? ")
if playing.lower() == "random access memory":
   print ("Great it is correct answer, you are going to fourth question")
   score += 1
else: 
   print ("sorry it is incorrect answer")

playing = input("what does PSU stands for? ")
if playing.lower() == ("power supply unit"):
   print ("Great it is correct answer ")
   score += 1

else:
   print ("sorry it is incorrect answer")


print ("Great it is correct answer, your score is " + str(score) + " awesome! ")

print ("great your percentage is " + str( score / 4 *100) + "%" )