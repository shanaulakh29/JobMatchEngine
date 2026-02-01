FROM python:3.12-slim

WORKDIR /

# system deps for postgres
RUN apt-get update && apt-get install -y build-essential libpq-dev 

# install dependencies
COPY docker-requirements.txt .
RUN pip install --no-cache-dir -r docker-requirements.txt

COPY worker /worker

# executables
CMD [ "celery", "-A", "worker.celery_app.celery", "worker", "--loglevel=info" ]
