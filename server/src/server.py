import sys
import os
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from Routes.mainRouter import mainRouter
from fastapi.middleware.cors import CORSMiddleware
origins = [
    "*"
]
load_dotenv()

HOST = os.getenv("SERVER_HOST")
PORT = int(os.getenv("PORT"))

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(mainRouter,prefix='/api')



def main():
    uvicorn.run("server:app", host=HOST, port=PORT, reload=True)
if __name__ == "__main__":
    main()