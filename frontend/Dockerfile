FROM ubuntu:20.04

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y python3.9 python3.9-dev python3-pip

COPY ../requirements.txt .

RUN pip install -r requirements.txt

COPY frontend/ .

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
