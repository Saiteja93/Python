import logging
import os
import uuid
from ensurepip import bootstrap
from typing import List
from dotenv import load_dotenv
from fastapi import FastAPI,status
from contextlib import asynccontextmanager
from faker import Faker
from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError
from kafka import KafkaProducer
from commands import CreatePeopleCommand
from entities import Person

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger()
load_dotenv(verbose=True)

producer: KafkaProducer = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global producer

    client = KafkaAdminClient(bootstrap_servers=os.environ['BOOTSTRAP_SERVERS'])
    topic= NewTopic(
        name=os.environ['TOPICS_PEOPLE_ADV_NAME'],
        num_partitions=int(os.environ['TOPICS_PEOPLE_ADV_PARTITIONS']),
        replication_factor=int(os.environ['TOPICS_PEOPLE_ADV_REPLICAS'])
    )

    try:
        client.create_topics(new_topics=[topic], validate_only=False)
        logger.info(f"Kafka topics created {topic.name}")

    except TopicAlreadyExistsError:
        logger.warning(f"Topics already exists {topic.name}")
    finally:
        client.close()

    producer = KafkaProducer(
        bootstrap_servers=os.environ['BOOTSTRAP_SERVERS'],
        linger_ms=int(os.environ['TOPICS_PEOPLE_ADV_LINGER_MS']),
        retries=int(os.environ['TOPICS_PEOPLE_ADV_RETRIES']),
        max_in_flight_requests_per_connection=int(os.environ['TOPICS_PEOPLE_ADV_INFLIGHT_REQS']),
        acks=os.environ['TOPICS_PEOPLE_ADV_ACK']
    )
    yield
    producer.close()
    logger.info("Kafka producer closed")


"""
def make_producer():
    return KafkaProducer(bootstrap_servers=os.environ['BOOTSTRAP_SERVERS'],
                         linger_ms = int(os.environ['TOPICS_PEOPLE_ADV_LINGER_MS']),
                         retries = int(os.environ['TOPICS_PEOPLE_ADV_RETRIES']),
                         max_in_flight_requests_per_connection = int(os.environ['TOPICS_PEOPLE_ADV_INFLIGHT_REQS']),
                         acks = os.environ['TOPICS_PEOPLE_ADV_ACK'])
"""


class SuccessHandler:
    def __init__(self,person):
        self.person = person

    def __call__(self, rec_metadata):
        logger.info(f"""
        successfully produced
        person {self.person}
        to topic {rec_metadata.topic}
        and partition {rec_metadata.partition}
        at offset {rec_metadata.offset}
        """)

class ErrorHandling:
    def __init__(self, person):
        self.person = person
    def __call__(self, ex):
        logger.error(f"Failed producing person {self.person}", exc_info = ex)



app = FastAPI(lifespan=lifespan)

@app.post("/api/people", status_code=201, response_model=List[Person] )
async def create_people(cmd: CreatePeopleCommand):
    global producer
    people: List[Person] = []

    faker = Faker()


    for _ in range(cmd.count):
        person = Person(id=str(uuid.uuid4()), name= faker.name(), title = faker.job().title())
        people.append(person)
        producer.send(topic=os.environ['TOPICS_PEOPLE_ADV_NAME'],
                      key = person.title.lower().replace(r's+', '-').encode('utf-8'),
                      value = person.model_dump_json().encode('utf-8'))\
                      .add_callback(SuccessHandler(person))\
                      .add_errback(ErrorHandling(person))

    producer.flush()
    return people

