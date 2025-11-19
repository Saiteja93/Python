
import random
students = {
    "Alex", "Ram", "Stella", "Areena", "shabia", "Arun", "kiran", "Max", "Jenny", "Austin"
}

scores_students = {student : random.randint(1,100) for student in students  }
print(f"students score ----> {scores_students}\n")
passed_students = {key : value for (key,value) in scores_students.items() if value >= 60 }
print(f"passed students ----> {passed_students}")


name = "himaja"
ovels = ["a", "e", "i", "o", "u"]

final_list = {v : 0 for v in ovels}

for ch in name:
    if ch in ovels:
        final_list[ch]+= 1


print(final_list)







