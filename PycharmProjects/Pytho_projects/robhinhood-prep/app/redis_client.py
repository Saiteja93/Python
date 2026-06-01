import redis
import os
from dotenv import load_dotenv


load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST","127.0.0.1")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
#connect to redis
redis_client = redis.Redis(
    host = REDIS_HOST,
    port = REDIS_PORT,
    decode_responses = True
)