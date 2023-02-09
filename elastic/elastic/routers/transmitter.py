# using fastapi router
from nis import cat
from fastapi import APIRouter
router = APIRouter()

# define json data format
from pydantic import BaseModel
from typing import Optional
import json

# using elasticsearch database (elasic cloud)
import elasticsearch

# load dotenv data
import os
from dotenv import load_dotenv

# set values
load_dotenv()
CLOUD_ID = os.getenv("CLOUD_ID")
CLOUD_USER = os.getenv("CLOUD_USER")
CLOUD_PSWD = os.getenv("CLOUD_PSWD")

# attach to the elasticserach database
es = elasticsearch.Elasticsearch(
    cloud_id=CLOUD_ID,
    http_auth=(CLOUD_USER, CLOUD_PSWD),
)

# define the json data format
class Item(BaseModel):
    sitename : Optional[str]
    url : Optional[str]
    title : Optional[str]
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
    
""" Example Request Body
{
    "0": {
        "sitename": "SEEK",
        "url": "https:\/\/www.seek.com.au\/job\/60157989?type=promoted",
        "title" : "Receptionists (Administration & Office Support)",
        "collectiondate": "1675836363",
        "startdate": "1675836363",
        "enddate": "",
        "companyname": "The Trustee for the Dr Maree Wilkins practice trust",
        "location": "Gladesville, Sydney NSW",
        "recruitfield": "",
        "recruittype": "",
        "recruitclassification": "",
        "personnel": "",
        "salary": "",
        "position": "Receptionists (Administration & Office Support)",
        "task": "",
        "qualifications": "",
        "prefer": "",
        "welfare": "",
        "description": "Which of the following statements best describes your right to work in Australia?"
    }
}
"""
    
# elastic router. Send json data to elastic cloud
@router.post("/elastic")
async def elastic(data : dict):
    try:
        for key, value in data.items():
            res = es.index(index="crawl_database", id=key, body=value)
            print(res)
        return res
    except Exception as e:
        return e