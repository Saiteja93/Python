
'''
import csv

with open ("./practice/CSV/weather_data.csv") as data_file:
    data = csv.reader(data_file)
    temparature = []
    for row in data:
        if row[1] != 'temp':
            temparature.append(row[1])

    print(temparature)
    '''
'''
import pandas

data = pandas.read_csv("./input/practice/CSV/weather_data.csv")

monday = data[data.day =="Monday"]
monday_temp = monday.condition
print(monday_temp)


dict_score = {
    "students" : ["sai", "teja", "guvvala"],
    "scores" : [70,69,54]
    }

score = pandas.DataFrame(dict_score)
print(score)
'''

import pandas

data = pandas.read_csv("./Input/practice-1/CSV/2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv")
Gray_squirrel = data[data["Primary Fur Color"] == "Gray"]
black_squirrel = data[data["Primary Fur Color"] == "Black"]
cinnamon_squirrel = data[data["Primary Fur Color"] == "Cinnamon"]
gray_len = (len(Gray_squirrel))
black_len = (len(black_squirrel))
cinnamon_len = len(cinnamon_squirrel)

data_dict = {
    "Fun color" : ["Gray", "Black", "Cinnamon"], 
    "Count" : [gray_len, black_len, cinnamon_len]

}

df = pandas.DataFrame(data_dict)
print(df)
df.to_csv("squirrel_count.csv")

             

                            




