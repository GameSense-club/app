import os
import requests
from logging_config import logger

def create_token(dir):
    file_path = os.path.join(dir, "token.txt")
    if not os.path.exists(file_path):
        url = "https://api.game-sense.ru/pc/register"
        headers = {"Content-Type": "application/json"}
        response = requests.get(url, headers=headers)
        response_data = response.json()
        token = response_data["token"]
        with open(file_path, 'w') as f:
            f.write(token)
        logger.info(f"Создан новый токен: {token}")

    else:
        with open(file_path, 'r') as f:
            token = f.read().strip()
        logger.info("Используется существующий токен.")

    return token