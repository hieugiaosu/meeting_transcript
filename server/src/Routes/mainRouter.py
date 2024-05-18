from fastapi import APIRouter
from Routes.connection.connection_controller import connectionController

mainRouter = APIRouter()
mainRouter.include_router(connectionController,prefix='')