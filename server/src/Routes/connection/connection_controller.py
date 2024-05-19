from fastapi import APIRouter
from DTO.etablishConnectionDTO import EtablishConnectionDTO
from Services.connection.connection_service import *
connectionController = APIRouter()

@connectionController.get("/",response_model=EtablishConnectionDTO,status_code=200)
async def connectionEstablish():
    return await newSecretId()