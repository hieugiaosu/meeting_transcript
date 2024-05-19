import uuid
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from utils.bridge import redis_client
import json
import time

async def newSecretId():
    secret_id = str(uuid.uuid4())
    res = jsonable_encoder({'secret_id':secret_id})
    currtime = int(time.time())
    redis_client.set(
        secret_id,
        json.dumps(
            {
                "access_at":currtime,
            }),
            exat=currtime+300)
    return JSONResponse(res)

async def checkID(secret_id):
    res = redis_client.get(secret_id)
    if res: 
        redis_client.expireat(secret_id,int(time.time())+300,gt=True)
    else: 
        raise HTTPException(401)
    res = json.loads(res)
    res['secret_id'] = secret_id
    return res