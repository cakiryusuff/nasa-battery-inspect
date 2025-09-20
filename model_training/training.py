import pandas as pd
import numpy as np
from datetime import datetime
from scipy.io import loadmat
from ydf import RandomForestLearner, Task
from config.paths_config import *
from utils.functions import get_data_from_gbucket
from src.logger import get_logger
import time

logger = get_logger(__name__)

class Training:
    def __init__(self):
        logger.info("-"*50)
        logger.info("Training started")
        self.model = None
        self.train_data_path = TRAIN_DATA_PATH
        self.model_path = MODEL_SAVE_PATH
        self.test_data_path = TEST_DATA_PATH
        
    def mat_to_dataframe(self, data_path: str) -> pd.DataFrame:
        dirs = os.listdir(data_path)
        for dir in dirs:
            if dir.endswith(".mat"):
                battery_key = dir.split(".")[0]
        battery_key = dirs[0].split(".")[0]
        logger.info(f"- Converting {battery_key}.mat to dataframe...")
        mat = loadmat(data_path + f"/{battery_key}.mat", squeeze_me=True, struct_as_record=False)
        block = mat[battery_key]

        records = []
        for c in block.cycle:
            if c.type != "discharge":
                continue

            records.append({
                "type": c.type,
                "ambient_temperature": c.ambient_temperature,
                "time": c.time,
                "Voltage_measured": c.data.Voltage_measured,
                "Current_measured": c.data.Current_measured,
                "Temperature_measured": c.data.Temperature_measured,
                "Current_charge": c.data.Current_load,
                "Voltage_charge": c.data.Voltage_load,
                "Time": c.data.Time,
                "Capacity": c.data.Capacity,
            })
        
        logger.info(f"- - {battery_key}.mat converted to dataframe")
        return pd.DataFrame(records)
    
    def datetime_to_timestamp(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("- Converting datetime to timestamp...")
        def mat2datetime(row):
            return datetime(
                int(row.time[0]), int(row.time[1]), int(row.time[2]), int(row.time[3]), int(row.time[4]), int(row.time[5])
            )
            
        df["time"] = df.apply(mat2datetime, axis=1)
        logger.info("- - Datetime converted to timestamp")
        return df

    def calc_soc(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("- Calculating SOC...")
        def calc_soc_fun(time_discharge, current_discharge, capacity):
            if isinstance(time_discharge, float) or capacity is None:
                return np.nan
            dt = np.diff(time_discharge, prepend=0) 
            charge_consumed = np.cumsum(np.abs(current_discharge) * dt) / (3600)
            soc = 1 - charge_consumed / capacity
            return soc

        df["soc"] = df.apply(lambda x: calc_soc_fun(x["Time"], x["Current_charge"], x["Capacity"]), axis=1)
        
        logger.info("- - SOC calculated")
        return df

    def equalize_data(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("- Equalizing data...")
        def equalize(voltages, target_len):
            if type(voltages) is float or len(voltages) < 2:
                return np.full(target_len, np.nan)
            if len(voltages) == target_len:
                return voltages
            
            return np.interp(np.linspace(0, 1, target_len), np.linspace(0, 1, len(voltages)), voltages)

        target_len = df["Time"].apply(lambda x: len(x)).max() #get max Time length

        df["Voltage_measured"] = df.apply(lambda x: equalize(x["Voltage_measured"], target_len), axis=1)
        df["Current_charge"] = df.apply(lambda x: equalize(x["Current_charge"], target_len), axis=1)
        df["Temperature_measured"] = df.apply(lambda x: equalize(x["Temperature_measured"], target_len), axis=1)
        df["Voltage_charge"] = df.apply(lambda x: equalize(x["Voltage_charge"], target_len), axis=1)
        df["Current_measured"] = df.apply(lambda x: equalize(x["Current_measured"], target_len), axis=1)
        df["Time"] = df.apply(lambda x: equalize(x["Time"], target_len), axis=1)
        df["soc"] = df.apply(lambda x: equalize(x["soc"], target_len), axis=1)
        
        logger.info("- - Data equalized")
        return df

    def explode_data(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("- Exploding data...")
        cols_to_explode = df.drop(["type", "time", "ambient_temperature", "Capacity"], axis=1).columns.tolist()
        df = df.explode(cols_to_explode)
        logger.info("- - Data exploded")
        return df

    def convert_obj_to_numeric(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("- Converting object columns to numeric...")
        cols = df.drop(["type", "time", "ambient_temperature"], axis=1).select_dtypes(include='object').columns
        df[cols] = df[cols].apply(pd.to_numeric)
        logger.info("- - Object columns converted to numeric")
        return df

    def feature_eng(self, df) -> pd.DataFrame:
        logger.info("- Performing feature engineering...")
        df['Power'] = df['Voltage_measured'] * df['Current_measured']
        df['C_rate'] = abs(df['Current_measured']) / df['Capacity']
        logger.info("- - Feature engineering completed")
        return df
    
    def prepare_data(self, data_path: str, target: str = "train") -> pd.DataFrame:
        logger.info("- Preparing data...")
        try:
            get_data_from_gbucket(target=target)
        except Exception as e:
            logger.error("- - Error getting data from GBucket: " + str(e))
            logger.info("- - Data not found in GBucket. Using local data")

        df = self.mat_to_dataframe(data_path)
        df = self.datetime_to_timestamp(df)
        df = self.calc_soc(df)
        df = self.equalize_data(df)
        df = self.explode_data(df)
        df = self.convert_obj_to_numeric(df)
        df = self.feature_eng(df)
        df = df[["Time", "Temperature_measured", "Power", "Voltage_measured", "Voltage_charge", "Current_measured", "soc"]] #this colums are got from notebook
        logger.info("Data prepared")
        
        return df
            
    def train(self, df: pd.DataFrame):
        logger.info("Training model...")
        df.fillna(0, inplace=True)
        start_time = time.time()
        self.model = RandomForestLearner(label="soc", task=Task.REGRESSION).train(df)
        logger.info(f"- Model trained. Training time: {time.time() - start_time} seconds")
        
    def evaluate(self, test_df: pd.DataFrame):
        logger.info("Evaluating model...")
        evaluation = self.model.evaluate(test_df)
        logger.info(f"- Model evaluated {evaluation}")
        return evaluation
        
    def save_model(self, model_path: str):
        logger.info("Saving model...")
        self.model.save(model_path + f"/{datetime.now().strftime('%Y%m%d%H%M%S')}")
        logger.info("- Model saved. Model path: " + model_path + f"{datetime.now().strftime('%Y%m%d%H%M%S')}")
    
    def save_test_data(self, test_df: pd.DataFrame, model_path: str):
        logger.info("Saving test data...")
        os.makedirs(model_path, exist_ok=True)
        test_df.to_csv(model_path + "/test_data.csv", index=False)
        logger.info("- Test data saved. Test data path: " + model_path + "/test_data.csv")
    
    def run(self):
        try:
            logger.info("Running training...")
            train_df = self.prepare_data(self.train_data_path)
            test_df = self.prepare_data(self.test_data_path, target="test")
            self.train(train_df)
            self.evaluate(test_df)
            self.save_model(self.model_path)
            self.save_test_data(test_df, self.test_data_path)
            logger.info("Training completed")
            logger.info("-"*50)
        except Exception as e:
            logger.error("Error running training: " + str(e))
            logger.info("-"*50)
                
if __name__ == "__main__":
    training = Training()
    training.run()
        