import pika
from pika import PlainCredentials
import os 
from dotenv import load_dotenv
import redis

load_dotenv()
rabbit_mq_connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=os.getenv("RABBIT_MQ_HOST"),
        port=os.getenv("RABBIT_MQ_PORT"),
        credentials=PlainCredentials(os.getenv("RABBIT_MQ_USER"),os.getenv("RABBIT_MQ_PASSWORD"))
    )
)
rabbit_mq_client = rabbit_mq_connection.channel()
rabbit_mq_client.queue_declare(queue="whisper_inference")
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"), 
    port=os.getenv("REDIS_PORT")
)
gen_redis_key = lambda x,y: f"ps:{x}-sk:{y}"