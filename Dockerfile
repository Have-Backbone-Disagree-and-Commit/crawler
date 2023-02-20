FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

<<<<<<< Updated upstream
COPY ./app /code/app

#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
CMD ["uvicorn", "app.elastic.elastic.main:app", "--host", "0.0.0.0", "--port", "80"]
=======
COPY ./elastic /code/elastic

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
CMD ["uvicorn", "elastic.elastic.main:app", "--host", "0.0.0.0", "--port", "80"]
>>>>>>> Stashed changes

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]