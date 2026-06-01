import json
from kafka import KafkaConsumer
import psycopg2

KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "trade-events"
GROUP_ID = "trade-processor-group-v2"

DB_CONFIG = {
    "host": "127.0.0.1",
    "database": "brokerage",
    "user": "admin",
    "password": "secret",
    "port": 5433,
}

def json_deserializer(data: bytes) -> dict:
    return json.loads(data.decode("utf-8"))

def save_trade(event: dict):
    try:

        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO trades(trade_id,symbol,side,quantity,price, total_value) VALUES(%s, %s,%s, %s,%s,%s)",
            (
                event.get("trade_id"),
                event.get("symbol"),
                event.get("side"),
                event.get("quantity"),
                event.get("price"),
                event.get("total_value")
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
    except psycopg2.errors.UniqueViolation:
        print(f"Duplicate trade detected: {event.get('trade_id')} - skipping")
        conn.rollback()
        conn.close()


consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers = KAFKA_BROKER,
    value_deserializer = json_deserializer,
    group_id = GROUP_ID,
    auto_offset_reset = "latest",
    enable_auto_commit = False
    )

if __name__ == "__main__":

    try:
        for message in consumer:
           print(f"partition={message.partition} offset={message.offset} value={message.value}")

           try:
               save_trade(message.value)
               consumer.commit()# only commit after succesfuk save
               print(f" Trade saved to db: {message.value['trade_id']}")
           except Exception as e:
               print(f"Failed to save trade: {e} - will retey")

            
    except KeyboardInterrupt:
        print("\n Consumer stopped by user")
    
    finally:
        consumer.close()
        


    