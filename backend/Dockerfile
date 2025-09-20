FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive 

# if u want to use Google Cloud Bucket on your local container,
# then uncomment this and make sure the service account key name is key.json
# ENV GOOGLE_APPLICATION_CREDENTIALS=/app/key.json

ENV DB_NAME=mydatabase
ENV DB_USER=myuser
ENV DB_PASSWORD=mypassword
ENV DB_HOST=myhost

RUN apt-get update && apt-get install -y python3.9 python3.9-dev python3-pip

WORKDIR /app

COPY . /app

RUN pip install -e .

RUN pip install gunicorn

RUN ["python3", "model_training/training.py"]

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "backend.app:app"]