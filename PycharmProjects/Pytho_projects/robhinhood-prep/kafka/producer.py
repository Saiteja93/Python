import json
from kafka import KafkaProducer
from random import randint,choice,uniform
import uuid

KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "trade-events"
STOCKS = ["AAPL","GOOGL","TSLA","AMZN","HOOD"]


def json_serializer(data: dict) -> bytes:
    return json.dumps(data).encode("utf-8")


producer = KafkaProducer(
 bootstrap_servers = KAFKA_BROKER,
 value_serializer = json_serializer    
)

ticker = choice(STOCKS)
def build_trade(ticker):
    quantity = randint(1,100)
    price = round(uniform(50.0, 500.0), 2)

    return {
        "trade_id": str(uuid.uuid4()),
        "symbol":ticker,
        "side": choice(["buy","sell"]),
        "quantity":quantity,
        "price": price,
        "total_value": round(quantity * price, 2)


    }

if __name__=="__main__":
    for i in range(10):
        print(f"Producer sending data to topic {KAFKA_TOPIC}")
        ticker = choice(STOCKS)
        event = build_trade(ticker)
        print(f"\nsending{event["side"]} {event["quantity"]} X {ticker}")
        producer.send(
            KAFKA_TOPIC,
            key=ticker.encode("utf-8"),
            value=event
        )
    
    producer.flush()
    print("Done")