import json
import time
import paho.mqtt.client as mqtt
import requests
import logging

logging.basicConfig(level=logging.INFO)

BROKER = "mqtt"
TOPIC = "battery/data"
BACKEND_URL = "http://backend:5000/return_prediction"

def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    while True:
        try:
            r = requests.post(BACKEND_URL, json=data)
            logging.info(f"Data: {data}")
            logging.info(f"SoC Prediction: {r.json()}")
            break
        except requests.exceptions.ConnectionError:
            print("Backend hazır değil, tekrar deniyor...")
            time.sleep(2)

client = mqtt.Client()
client.on_message = on_message
client.connect(BROKER, 1883, 60)
client.subscribe(TOPIC)
client.loop_forever()
