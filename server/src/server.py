import sys
import os
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from Routes.mainRouter import mainRouter
from Middelware.Middlware import middlewareList
load_dotenv()

HOST = os.getenv("SERVER_HOST")
PORT = int(os.getenv("PORT"))

app = FastAPI()
for middleware in middlewareList:
    app.add_middleware(**middleware)
app.include_router(mainRouter,prefix='/api')



def main():
    uvicorn.run("server:app", host=HOST, port=PORT, reload=True)
if __name__ == "__main__":
    main()