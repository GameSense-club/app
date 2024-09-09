import requests
import os

# Конфигурация
GITHUB_API_URL = "https://api.github.com"
REPO_OWNER = "Falbue"  # Ваш логин на GitHub
REPO_NAME = "GameSense-App"  # Имя репозитория
ACCESS_TOKEN = "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"  # Ваш токен доступа
LOCAL_DIR = os.getcwd()  # Локальная папка для сохранения файлов (текущая директория)

# Получение содержимого директории
def get_contents(path=""):
    url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/contents/{path}"
    headers = {
        "Authorization": f"token {ACCESS_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка при получении содержимого: {response.status_code}")
        return None

# Скачивание всех файлов по ссылке
def download_files(contents):
    for item in contents:
        if item['type'] == 'file':
            download_file(item['download_url'], item['name'])
        elif item['type'] == 'dir':
            # Если элемент - директория, рекурсивно получить содержимое
            sub_contents = get_contents(item['path'])
            if sub_contents:
                download_files(sub_contents)

# Скачивание файла по raw-ссылке
def download_file(file_url, file_name):
    local_path = os.path.join(LOCAL_DIR, file_name)
    response = requests.get(file_url)
    if response.status_code == 200:
        with open(local_path, 'wb') as f:  # Сохраняем в бинарном режиме
            f.write(response.content)
        print(f"Файл {file_name} успешно скачан и сохранён как {local_path}")
    else:
        print(f"Ошибка при скачивании {file_name}: {response.status_code}")

# Основная логика
def main():
    contents = get_contents()
    if contents:
        download_files(contents)

if __name__ == "__main__":
    main()
