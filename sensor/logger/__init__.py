import logging
from datetime import datetime
import os
from pathlib import Path


PROJECT_DIR = Path("sensor").absolute().resolve()
LOGS_DIR = os.path.join(PROJECT_DIR,"logs")
os.makedirs(LOGS_DIR, exist_ok= True)

def get_log_file_name():
    return f"log_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log"

LOG_FILE_NAME=get_log_file_name()

os.makedirs(LOGS_DIR,exist_ok=True)

LOG_FILE_PATH = os.path.join(LOGS_DIR,LOG_FILE_NAME)

logging.basicConfig(filename=LOG_FILE_PATH,
filemode="w",
format="[%(asctime)s - %(levelname)s - %(name)s - %(module)s - %(funcName)s - %(lineno)d] : %(message)s",
level=logging.INFO,
)