import uvicorn
from fastapi import FastAPI
import csv
import os
from dotenv import load_dotenv
from .routers import transmitter

# using dotenv
load_dotenv()

app = FastAPI()
# routing
app. include_router(transmitter.router)

def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("elastic.main:app", host="0.0.0.0", port=8000, reload=True)