from utils.bridge import rabbit_mq_client
from pika import BasicProperties
import time

def handler(ch,method,properties:BasicProperties,body):
    time.sleep(2)
    print(f"message: {body}")

rabbit_mq_client.basic_qos(prefetch_count=1)
rabbit_mq_client.basic_consume(queue='whisper_inference', on_message_callback=handler)

rabbit_mq_client.start_consuming()