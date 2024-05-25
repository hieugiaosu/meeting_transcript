from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from utils.bridge import redis_client, rabbit_mq_client,gen_redis_key
from pika import BasicProperties
from DTO.redisDTO import *
from DTO.speechTranscriptDTO import *
import json
import pickle


async def transcript_producer(user_info:AccountInfoDTO,req:SpeechTranscriptDTORequest):
    audio = await req.audio.read()
    data = json.loads(audio)
    audio = list(map(float,eval(data) if isinstance(data,str) else data))
    rabbit_mq_client.basic_publish(
        exchange="",
        routing_key="whisper_inference",
        body=pickle.dumps(audio),
        properties=BasicProperties(headers={
            "secret_id":user_info['secret_id'],
            "request_number": req.request_number,
            "sample_rate": req.sample_rate,
            "end_request": req.end_request
        })
    )

async def get_transcript_result(secret_id:str,data:GetTranscriptDTO):
    start_num = int(data.from_number)
    end_num = int(data.to_number)
    speaker_res = []
    transcript_res = []
    chunk_idx = start_num-1
    for i in range(start_num,end_num+1):
        key = gen_redis_key(secret_id,i)
        transcript = redis_client.get(key)
        if transcript is None:
            break
        transcript = dict(json.loads(transcript))
        speaker_res.append(transcript['speaker'])
        transcript_res.append(transcript['transcript'])
        chunk_idx = i
    res = {
        "from_number": start_num, 
        "to_number": chunk_idx,
        "speakers": speaker_res,
        "transcript": transcript_res
    }
    res = jsonable_encoder(res)
    return JSONResponse(res)