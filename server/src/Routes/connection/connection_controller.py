from fastapi import APIRouter
from DTO.test_dto import TestDTO
from Services.testService import test
connectionController = APIRouter()

@connectionController.get("/",response_model=TestDTO,status_code=200)
async def connectionEstablish():
    test()
    return TestDTO()