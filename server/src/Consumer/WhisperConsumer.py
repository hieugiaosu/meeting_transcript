import sys 
sys.path.append('C:/Users/User/Documents/cinnamon/server/src')
from utils.bridge import rabbit_mq_client, redis_client
from utils.whisperInference import WhisperInference
from pika import BasicProperties
import time
import json
import pickle

whisper = WhisperInference()

def handler(ch,method,properties:BasicProperties,body):
    global whisper
    audio = pickle.loads(body)
    sample_rate = properties.headers['sample_rate']
    secret_id = properties.headers["secret_id"]
    request_number = properties.headers["request_number"]
    end_request = properties.headers["end_request"]
    currtime = int(time.time())
    transcript = whisper(audio,sample_rate)
    print(transcript)
    redis_client.set(
        f"ps:{secret_id}-sk:{request_number}",
        json.dumps({"transcript":transcript,"speaker":1,"end_request":end_request}),
        exat=currtime+600
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)

rabbit_mq_client.basic_qos(prefetch_count=1)
rabbit_mq_client.basic_consume(queue='whisper_inference', on_message_callback=handler)

rabbit_mq_client.start_consuming()