
users = [
    {"id":1, "total": 100, "coupoun":"P20"},
    {"id":2, "total": 150, "coupoun":"P10"},
    {"id":3, "total": 80, "coupoun":"P50"}
]

discount = {
    "P20": (0.2,0),
    "P10" : (0.5,0),
    "P50" : (0,10)
}

for user in users:
    percentage, fixed = discount.get(user["coupoun"], (0,0))
    next_discount = user["total"] * percentage + fixed
    
    print(f"{user["id"]} total bill is {user["total"]}, next time you will get this discount {next_discount} ")
