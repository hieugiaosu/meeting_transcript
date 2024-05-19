from fastapi import APIRouter
from Routes.connection.connection_controller import connectionController
from Routes.transcription.transcription_controller import transcription_controller

mainRouter = APIRouter()
mainRouter.include_router(connectionController,prefix='')
mainRouter.include_router(transcription_controller,prefix='/speech')