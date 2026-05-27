import json
from kafka import KafkaProducer
from random import randint,choice,uniform

KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "trade-events"
STOCKS = ["APPL","GOOGL","TSLA","AMZN","HOOD"]


def json_serializer(data: dict) -> bytes:
    return json.dumps(data).encode("utf-8")


producer = KafkaProducer(
 bootstrap_servers = KAFKA_BROKER,
 value_serializer = json_serializer    
)

ticker = choice(STOCKS)
def build_trade(ticker):
    
    action = choice(["BUY","SELL"])
    quantity = randint(1,100)
    price = round(uniform(50.0, 500.0), 2)

    return {
        "ticker":ticker,
        "action":action,
        "quantity":quantity,
        "price": price,
    }

if __name__=="__main__":
    for i in range(10):
        print(f"Producer sending data to topic {KAFKA_TOPIC}")
        ticker = choice(STOCKS)
        event = build_trade(ticker)
        print(f"sending{event["action"]} {event["quantity"]} X {ticker}")
        producer.send(
            KAFKA_TOPIC,
            key=ticker.encode("utf-8"),
            value=event
        )
    
    producer.flush()
    print("Done")