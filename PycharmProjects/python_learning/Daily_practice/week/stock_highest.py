stocks={"AAPL":154.54,"TSLA":123.65,"GOOG": 420.45,
        "MSFT":223.25, "AMZN": 23.15, "NFLX": 42.65}
def highest_stock(stocks):
    highest = max(stocks,key=stocks.get)
    return highest

highest = highest_stock(stocks)
print(f"highest price stock is {highest} and value is ${stocks[highest]}")