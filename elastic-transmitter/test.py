from tomllib import load
import elasticsearch
import csv
import os
from dotenv import load_dotenv

load_dotenv()

CLOUD_ID = os.getenv("CLOUD_ID")
CLOUD_USER = os.getenv("CLOUD_USER")
CLOUD_PSWD = os.getenv("CLOUD_PSWD")

es = elasticsearch.Elasticsearch(
    cloud_id="crawl:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyQxMzEzNzUzZjNhNGU0NGQ1YTYyNzE5YzkwNjA0Yzc0NiRiODhkZmNjNDU2ODU0Mjc1YjZiOWZiMzcwYmJkMWZkOQ==",
    http_auth=("elastic", "iZ4PQh7I8RVE8VuWQeyxielP"),
)

with open("data.csv") as file:
    reader = csv.reader(file)
    for i, row in enumerate(reader):
        # Create a dictionary for each row with default column names
        document = {f"column{j}": value for j, value in enumerate(row)}
        # Save each row as a separate document in Elasticsearch
        es.index(index="my_index", id=i, body=document)