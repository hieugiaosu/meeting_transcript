from fastapi import APIRouter, Depends
from DTO.speechTranscriptDTO import *
from Services.connection.connection_service import checkID
from Services.transcription.trainscription_service import *
transcription_controller = APIRouter()


"""
The api endpoint for doing the transcript
parameters:
request_number: the idx of the of the audio chunk (for detect the order)
end_request: determine if this chunk is the last or not
audio: a json file contain a array after read the audio (using xenova for webclient)
sample_rate: sample_rate of audio
"""
@transcription_controller.post("/{secret_id}",status_code=202)
async def requestTranscript(
    secret_id:str,
    data: SpeechTranscriptDTORequest = Depends(SpeechTranscriptDTORequest.as_form)
    ):
    account = await checkID(secret_id)
    # if not data.end_request:
    await transcript_producer(account,data)
    return {'message':'received'}

@transcription_controller.put("/{secret_id}",status_code=200,response_model=SpeechTranscriptResponse)
async def getTranscript(secret_id:str,data:GetTranscriptDTO):
    account = await checkID(secret_id)
    return await get_transcript_result(secret_id,data)