import os

BUCKET_NAME = "yed_interview_bucket"
ARTIFACTS_DIR = "artifacts/"
DATA_DIR = "data/"
TRAIN_DATA_DIR = "data/train"
TEST_DATA_DIR = "data/test"
MODELS_DIR = "models/"

MODEL_SAVE_PATH = os.path.join(ARTIFACTS_DIR, MODELS_DIR)
TRAIN_DATA_PATH = os.path.join(ARTIFACTS_DIR, TRAIN_DATA_DIR)
TEST_DATA_PATH = os.path.join(ARTIFACTS_DIR, TEST_DATA_DIR)