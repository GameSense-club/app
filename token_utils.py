import os
import jwt
import requests
import secrets
import string

APPDATA_DIR = os.getenv('LOCALAPPDATA')
DIR = os.path.join(APPDATA_DIR, "Programs", "GameSense")
FILE = os.path.join(DIR, "token.txt")

def generate_random_token(length=32):
    characters = string.ascii_letters + string.digits + '-_'
    return ''.join(secrets.choice(characters) for _ in range(length))


def create_token(file_path=FILE):
    if not os.path.exists(file_path):
        token = jwt.encode({
            'user_id': 'computer',
            'email': generate_random_token(),
            'role': 'developer'
        }, "GhonseMaskot", algorithm="HS256")
    
        with open(file_path, 'w') as f:
            f.write(token)
        print(f"Создан новый токен: {token}")

        url = "https://api.game-sense.net/pc/register"
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)

    else:
        with open(file_path, 'r') as f:
            token = f.read().strip()
        print("Используется существующий токен.")

    return token