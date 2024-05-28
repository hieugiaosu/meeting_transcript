import sys
import os

# Determine the base directory
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add necessary directories to the system path
sys.path.append(os.path.join(base_dir))
sys.path.append(os.path.join(base_dir, 'utils', 'model_weight'))

from utils.bridge import rabbit_mq_client, redis_client
from utils.whisperInference import WhisperInference
from utils.SpeakerEmbedding import SpeakerEmbeddingInference
from pika import BasicProperties
import time
import json
import pickle
import torch

# Initialize models with relative paths
whisper = WhisperInference()
speakerEmb = SpeakerEmbeddingInference(os.path.join(base_dir, 'utils', 'model_weight', 'speaker_embedding.pth'))

def determineSpeaker(secret_id, e, currtime):
    threshold = 0.3
    speaker = 0
    userInfo = redis_client.get(secret_id)
    userInfo = json.loads(userInfo)
    if userInfo['speaker_list'] == []:
        print('first speaker @@@')
        userInfo['speaker_list'].append(e.squeeze().numpy().tolist())
    else: 
        speaker_list = torch.tensor(userInfo['speaker_list']).float() 
        cos = e @ speaker_list.T
        cos = cos.squeeze()
        print(cos)
        speaker = torch.argmax(cos, 0).item() if cos.dim() != 0 else 0
        similarity = cos[speaker].item() if cos.dim() != 0 else cos.item()
        if similarity < threshold:
            speaker = len(userInfo['speaker_list'])
            userInfo['speaker_list'].append(e.squeeze().numpy().tolist())
    redis_client.set(
        secret_id,
        json.dumps(userInfo),
        exat=currtime + 300
    )
    return speaker

def handler(ch, method, properties: BasicProperties, body):
    global whisper
    audio = pickle.loads(body)
    sample_rate = properties.headers['sample_rate']
    secret_id = properties.headers["secret_id"]
    request_number = properties.headers["request_number"]
    end_request = properties.headers["end_request"]
    currtime = int(time.time())
    
    e = speakerEmb(audio, sample_rate)
    speaker = determineSpeaker(secret_id, e, currtime)
    transcript = whisper(audio, sample_rate)
    
    redis_client.set(
        f"ps:{secret_id}-sk:{request_number}",
        json.dumps({"transcript": transcript, "speaker": speaker + 1, "end_request": end_request}),
        exat=currtime + 600
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)

rabbit_mq_client.basic_qos(prefetch_count=1)
rabbit_mq_client.basic_consume(queue='whisper_inference', on_message_callback=handler)

rabbit_mq_client.start_consuming()
