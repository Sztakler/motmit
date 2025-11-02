import logging
import datetime
import os

os.makedirs('logs', exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"logs/experiment_{timestamp}.txt"

logger = logging.getLogger('experiment')
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(filename)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.handlers = []
logger.addHandler(file_handler)

