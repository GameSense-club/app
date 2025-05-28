import os
import secrets
import requests

headers = {"Content-Type": "application/json", "x-api-key": "pc_keys"}

def create_token(file_path='token.txt'):
    if not os.path.exists(file_path):
        token = secrets.token_hex(16)
        with open(file_path, 'w') as f:
            f.write(token)
        print(f"Создан новый токен: {token}")
        data = {"token":token}
        response = requests.post(url, json=data, headers=headers)

    else:
        with open(file_path, 'r') as f:
            token = f.read().strip()
        print("Используется существующий токен.")

    return token