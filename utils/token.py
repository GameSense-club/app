import os
import requests
from . import logger

try: 
    import config
    DEBUG = config.DEBUG
    logger = logger.setup(True, "TOKEN", "data/")
except: 
    DEBUG = False
    logger = logger.setup(False, "APP", "data/")

def create_token(dir):
    file_path = os.path.join(dir, "token.txt")
    if not os.path.exists(file_path):
        url = "https://api.game-sense.ru/pc/registration"
        headers = {"Content-Type": "application/json"}
        response = requests.get(url, headers=headers)
        response_data = response.json()
        key = response_data["key"]
        os.makedirs(dir, exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(key)
        logger.info(f"Создан новый ключ доступа: {key}")

    else:
        with open(file_path, 'r') as f:
            key = f.read().strip()
        logger.debug("Используется существующий ключ доступа")

    return key