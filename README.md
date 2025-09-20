# Nasa Battery Inspect and SoC Prediction

## Train and Test data
The project automatically selects .mat files from the artifacts/data/test and artifacts/data/train folders. As long as the datasets have the same structure, you can replace them with your own data.

## Database Integration
```sh
#If you want to use Database Integration just change this part from backend/Dockerfile

ENV DB_NAME=mydatabase
ENV DB_USER=myuser
ENV DB_PASSWORD=mypassword
ENV DB_HOST=myhost

```

## Running the All Project
1. First of all you need to install Docker
2. Copy The Repo
```
git clone https://github.com/cakiryusuff/nasa-battery-inspect.git
cd nasa-battery-inspect
```
4. and then start all services:
```sh
#this phase might take a while 
docker compose up --build
```
3. Finally access the frontend with *localhost:8501* address

## Running the Model Training Alone:
1. You need to install dependencies, make sure you are on the same directory with setup.py file
2. Make sure you are using Virtual Env, Then
```
pip install -e .
```
```
python model_training/training.py
```
model weights will save to artifacts/data/models/*
