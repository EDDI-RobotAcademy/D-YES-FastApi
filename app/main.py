from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import os
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()
origins = os.getenv('origins')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get-origins")
def read_root():
    return os.getenv('origins')