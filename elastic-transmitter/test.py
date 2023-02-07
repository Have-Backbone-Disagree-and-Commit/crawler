import elasticsearch
import csv
import os
from dotenv import load_dotenv

load_dotenv()

CLOUD_ID = os.getenv("CLOUD_ID")
CLOUD_USER = os.getenv("CLOUD_USER")
CLOUD_PSWD = os.getenv("CLOUD_PSWD")

es = elasticsearch.Elasticsearch(
    cloud_id=CLOUD_ID,
    http_auth=(CLOUD_USER, CLOUD_PSWD),
)

with open("data.csv") as file:
    reader = csv.reader(file)
    for i, row in enumerate(reader):
        # Create a dictionary for each row with default column names
        document = {f"column{j}": value for j, value in enumerate(row)}
        # Save each row as a separate document in Elasticsearch
        res = es.index(index="my_index", id=i, body=document)
        print(res)