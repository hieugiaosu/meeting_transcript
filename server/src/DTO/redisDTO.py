from pydantic import BaseModel

class AccountInfoDTO(BaseModel):
    secret_id: str 
    access_at: int

class TranscriptInfoDTO(BaseModel):
    message_idx: int 
    transcript: str 
    speaker: str 
    is_end: bool