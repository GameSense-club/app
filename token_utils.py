import os
import requests

APPDATA_DIR = os.getenv('LOCALAPPDATA')
DIR = os.path.join(APPDATA_DIR, "GameSense")
FILE = os.path.join(DIR, "token.txt")

def create_token(file_path=FILE):
    if not os.path.exists(file_path):
        url = "https://api.game-sense.ru/pc/register"
        headers = {"Content-Type": "application/json"}
        response = requests.get(url, headers=headers)
        response_data = response.json()
        token = response_data["token"]
        with open(file_path, 'w') as f:
            f.write(token)
        print(f"Создан новый токен: {token}")

    else:
        with open(file_path, 'r') as f:
            token = f.read().strip()
        print("Используется существующий токен.")

    return token