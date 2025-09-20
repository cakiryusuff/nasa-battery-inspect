from google.cloud import storage
from config.paths_config import *
from src.logger import get_logger
import os

logger = get_logger(__name__)

def get_data_from_gbucket():
    logger.info("Downloading data from Google Cloud Storage...")
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blobs = bucket.list_blobs()

    for blob in blobs:
        relative_path = blob.name
        if not relative_path:
            continue
        
        os.makedirs(os.path.dirname(ARTIFACTS_DIR), exist_ok=True)

        local_path = os.path.join(ARTIFACTS_DIR, os.path.join(DATA_DIR, relative_path)) 
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        blob.download_to_filename(local_path)
        logger.info(f"- Downloaded {blob.name} to {local_path}")
    
    logger.info("- Data downloaded from Google Cloud Storage.")
        
def get_latest_model_dir() -> str:
    path = os.path.join(MODEL_SAVE_PATH, os.listdir(MODEL_SAVE_PATH)[-1])
    logger.info(f"Latest model directory: {path}")
    return path