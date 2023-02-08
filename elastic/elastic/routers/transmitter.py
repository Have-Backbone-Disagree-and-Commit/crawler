from typing import Optional
from fastapi import APIRouter, FastAPI, Body
router = APIRouter()
import os
import elasticsearch
from pydantic import BaseModel

from dotenv import load_dotenv
load_dotenv()

CLOUD_ID = os.getenv("CLOUD_ID")
print(CLOUD_ID)
CLOUD_USER = os.getenv("CLOUD_USER")
CLOUD_PSWD = os.getenv("CLOUD_PSWD")

es = elasticsearch.Elasticsearch(
    cloud_id="crawl:dXMtZWFzdC0yLmF3cy5lbGFzdGljLWNsb3VkLmNvbTo0NDMkNWFlNjQyNWRjNGJiNDRjNThlYjExMTdkMzVlNmQ0NGQkMjJjYjEwZTA2OTEzNDYyNzg1MTY4N2MzZGM3ZGExNTM=",
    http_auth=("elastic", "qFEupQHbmLZYFGT6jG8ZvRTm"),
)

class Item(BaseModel):
    sitename : Optional[str]
    url : Optional[str]
    collectiondate : Optional[str]
    startdate : Optional[str]
    enddate : Optional[str]
    companyname : Optional[str]
    location : Optional[str]
    recruitfield : Optional[str]
    recruittype : Optional[str]
    recruitclassification : Optional[str]
    personnel : Optional[str]
    salary : Optional[str]
    position : Optional[str]
    task : Optional[str]
    qualifications : Optional[str]
    prefer : Optional[str]
    welfare : Optional[str]
    description : Optional[str]
    stacks : Optional[str]
    

@router.post("/post")
async def post(data : dict):
    
    for key, value in data.items():
        res = es.index(index="jobs", id=key, body=value)
        
    print(res)
    return res
