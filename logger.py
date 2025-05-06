import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('experiment_log.txt')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)