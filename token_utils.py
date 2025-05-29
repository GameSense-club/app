import os
import jwt
import requests




def create_token(file_path='token.txt'):
    if not os.path.exists(file_path):
        token = jwt.encode({
            'user_id': 'computer',
            'email': 'gamesense.ghost@gmail.com',
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