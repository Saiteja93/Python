import requests
import json
stock_name = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY = "VJT73LXSLOHI8P3I"
NEW_API_KEY = "8d0c8e5396804e2a89a803afd2b6791f"



Stock_endpoint = "https://www.alphavantage.co/query"
News_endpoint = "https://newsapi.org/v2/everything"
STOCK_PARAMS= {
    "function" : "TIME_SERIES_DAILY",
    "symbol" : stock_name,
    "apikey" : STOCK_API_KEY,



}
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo'
response = requests.get(Stock_endpoint, params=STOCK_PARAMS)
data = response.json()["Time Series (Daily)"]
stock_list = [value for (key,value) in data.items()]
yesterday_closing_price = stock_list[0]["4. close"]
print(f"yesterdays closing price: {yesterday_closing_price}$")
day_before_yesterday_price = stock_list[1]["4. close"]
print(f"Day before closing price: {day_before_yesterday_price}$")
difference = float(yesterday_closing_price) - float(day_before_yesterday_price)
print(f"Price difference: {difference}")
up_down = None
if difference >0:
    up_down = "🔺"
else:
    up_down = "🔻"


price_change_percentage = (difference /float(yesterday_closing_price))*100
print(f"Percentage of change price: {price_change_percentage}%")

if price_change_percentage < 0:
    news_params= {
        "apiKey": NEW_API_KEY,
        "qInTitle": COMPANY_NAME,



    }
    news_response = requests.get(News_endpoint, params=news_params)
    news_data= news_response.json()["articles"]
    three_articles_data = news_data[:3]
    formatted_articles = [
        f"{stock_name}: {up_down}{price_change_percentage}%\n"
        f"Headline: {article['title']}. \n"
        f"Brief: {article['description']}"
        for article in three_articles_data
    ]
    for article in formatted_articles:
        print(article)
        print()






