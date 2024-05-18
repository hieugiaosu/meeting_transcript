import pika
from pika import PlainCredentials
import os 
from dotenv import load_dotenv
load_dotenv()


rabbit_mq_connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=os.getenv("RABBIT_MQ_HOST"),
        port=os.getenv("RABBIT_MQ_PORT"),
        credentials=PlainCredentials(os.getenv("RABBIT_MQ_USER"),os.getenv("RABBOT_MQ_PASSWORD"))
    )
)
rabbit_mq_client = rabbit_mq_connection.channel()
rabbit_mq_client.queue_declare(queue="whisper_inference")