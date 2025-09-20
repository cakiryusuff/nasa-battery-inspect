import json
import time
import paho.mqtt.client as mqtt
import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO)

BROKER = "mqtt"
TOPIC = "battery/data"

client = mqtt.Client()
client.connect(BROKER, 1883, 60)

df = pd.read_csv("test_data.csv")

for _, row in df.iterrows():
    payload = json.dumps({
            "Voltage_measured": row["Voltage_measured"],
            "Current_measured": row["Current_measured"],
            "Temperature_measured": row["Temperature_measured"],
            "Voltage_charge": row["Voltage_charge"],
            "Time": row["Time"],
            "Power": row['Voltage_measured'] * row['Current_measured'],
        })
    client.publish(TOPIC, payload)
    logging.info(f"Publishing data...")
    time.sleep(10)  # her saniye bir ölçüm
