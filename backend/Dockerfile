FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive 

ENV GOOGLE_APPLICATION_CREDENTIALS=/app/key.json

RUN apt-get update && apt-get install -y python3.9 python3.9-dev python3-pip

WORKDIR /app

COPY . /app

RUN pip install -e .

RUN pip install gunicorn

RUN ["python3", "model_training/training.py"]

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "backend.app:app"]