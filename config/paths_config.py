import os

BUCKET_NAME = "yed_interview_bucket"
ARTIFACTS_DIR = "artifacts/"
DATA_DIR = "data/"
MODELS_DIR = "models/"

MODEL_SAVE_PATH = os.path.join(ARTIFACTS_DIR, MODELS_DIR)
DATA_PATH = os.path.join(ARTIFACTS_DIR, DATA_DIR)
TEST_DATA_PATH = os.path.join(DATA_PATH, "test/")