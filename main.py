from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.api import router as api_router

from models import usermodel

app = FastAPI()
origins=["http://localhost",
         "http://localhost:8080",
         "http://localhost:8080",
         "http://localhost:5500",
         "http://127.0.0.1:5500",
         "http://127.0.0.1:5501",
         "https://eliasstein.github.io",
         "https://eliasstein.github.io/CodoACodo-MundoDeporte"
         ]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])
app.include_router(api_router)


@app.get("/",tags=["Hello world"])
def read_root():
    return {"Hola": "mundo"}


