from pydantic import BaseModel

class TestDTO(BaseModel):
    msg: str = "hello"