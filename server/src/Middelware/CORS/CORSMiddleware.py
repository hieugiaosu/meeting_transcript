from fastapi.middleware.cors import CORSMiddleware


origins = ["*"]
corsMiddleware = {
    "middleware_class": CORSMiddleware, 
    "options":{
        "allow_origins":origins,
        "allow_credentials":True,
        "allow_methods":["*"],
        "allow_headers":["*"],
    }
}