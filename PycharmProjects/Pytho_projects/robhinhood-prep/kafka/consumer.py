import json
from kafka import KafkaConsumer

KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "trade-events"
GROUP_ID = "trade-process-group"


def json_deserializer(data: bytes) -> dict:
    return json.loads(data.decode("utf-8"))



consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers = KAFKA_BROKER,
    value_deserializer = json_deserializer,
    group_id = GROUP_ID,
    auto_offset_reset = "earliest"
    



)
if __name__ == "__main__":

    try:
        for message in consumer:
           print(f"partition={message.partition} offset={message.offset} value={message.value}")
    except KeyboardInterrupt:
        print("\n Consumer stopped by user")
    
    finally:
        consumer.close()


    