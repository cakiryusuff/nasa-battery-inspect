import flask
import os
from ydf import load_model
from config.paths_config import *
from utils.functions import get_latest_model_dir
from src.db_manager import DBManager
app = flask.Flask(__name__)

model = load_model(get_latest_model_dir())

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

db_manager = DBManager(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST)
db_manager.connect()

@app.route("/return_prediction", methods=["POST", "GET"])
def index():
    if flask.request.method == "POST":
        data = flask.request.get_json()
        variable = {
            "Voltage_measured": [data["Voltage_measured"]],
            "Current_measured": [data["Current_measured"]],
            "Temperature_measured": [data["Temperature_measured"]],
            "Voltage_charge": [data["Voltage_charge"]],
            "Time":[data["Time"]],
            "Power": [data['Voltage_measured'] * data['Current_measured']],
        }
        predictions = model.predict(variable)

        db_manager.insert_prediction(data["Voltage_measured"], data["Current_measured"], data["Temperature_measured"], data["Voltage_charge"], data["Time"], data['Voltage_measured'] * data['Current_measured'], predictions[0])
        
        return flask.jsonify({"prediction": predictions.tolist()})
    else:
        return "Hello World!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    db_manager.close()