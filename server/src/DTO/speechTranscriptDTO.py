from pydantic import BaseModel
from dataclasses import dataclass
from typing import List
from fastapi import UploadFile,File,Form

class SpeechTranscriptDTORequest(BaseModel):
    request_number: int
    end_request: bool
    audio: UploadFile
    sample_rate: int
    @classmethod
    def as_form(
        cls,
        request_number: int = Form(...),
        end_request: bool = Form(...),
        sample_rate: int = Form(...),
        audio: UploadFile = File(...),
    ):
        return cls(
            request_number=request_number,
            sample_rate=sample_rate,
            end_request=end_request,
            audio=audio
            )

class SpeechTranscriptResponse(BaseModel):
    from_number: int 
    to_number: int
    speakers: List[str]
    transcript: List[str]

class GetTranscriptDTO(BaseModel):
    from_number: int 
    to_number: int