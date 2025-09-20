import flask
import os
from ydf import load_model
from config.paths_config import *
from utils.functions import get_latest_model_dir
from src.db_manager import DBManager
from src.logger import get_logger

logger = get_logger(__name__)
app = flask.Flask(__name__)

model = load_model(get_latest_model_dir())
use_db = True

try:
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")

    db_manager = DBManager(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST)
    db_manager.connect()
except Exception as e:
    use_db = False
    logger.info(f"Database connection failed, database is not using: {e}")

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
        
        if use_db:
            db_manager.insert_prediction(float(data["Voltage_measured"]), float(data["Current_measured"]), float(data["Temperature_measured"]), float(data["Voltage_charge"]), float(data["Time"]), float(data['Voltage_measured'] * data['Current_measured']), float(predictions[0]))
        
        return flask.jsonify({"prediction": predictions.tolist()})
    else:
        return "Hello World!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)