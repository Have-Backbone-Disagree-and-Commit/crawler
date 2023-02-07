from fastapi import APIRouter
router = APIRouter()
import os
import elasticsearch
from pydantic import BaseModel

from dotenv import load_dotenv
load_dotenv()

CLOUD_ID = os.getenv("CLOUD_ID")
CLOUD_USER = os.getenv("CLOUD_USER")
CLOUD_PSWD = os.getenv("CLOUD_PSWD")

es = elasticsearch.Elasticsearch(
    cloud_id="crawl:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyQxMzEzNzUzZjNhNGU0NGQ1YTYyNzE5YzkwNjA0Yzc0NiRiODhkZmNjNDU2ODU0Mjc1YjZiOWZiMzcwYmJkMWZkOQ==",
    http_auth=("elastic", "iZ4PQh7I8RVE8VuWQeyxielP"),
)

class Item(BaseModel):
    csv: str

@router.post("/get_test")
async def get_test(item : Item):
    return item
