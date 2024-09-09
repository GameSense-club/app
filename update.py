import requests
import base64
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

# Скачивание файла
def download_file(file_info):
    # Декодирование содержимого файла из base64
    content = base64.b64decode(file_info['content']).decode('utf-8')
    
    # Определение локального пути для сохранения файла
    local_path = os.path.join(LOCAL_DIR, file_info['name'])
    
    # Сохранение файла на локальный диск
    with open(local_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Файл {file_info['name']} успешно скачан и сохранён как {local_path}")

# Обработка содержимого директории
def process_contents(contents):
    for item in contents:
        if item['type'] == 'file':
            download_file(item)
        elif item['type'] == 'dir':
            # Если элемент - директория, рекурсивно получить содержимое
            sub_contents = get_contents(item['path'])
            if sub_contents:
                process_contents(sub_contents)

# Основная логика
def main():
    contents = get_contents()
    if contents:
        process_contents(contents)

if __name__ == "__main__":
    main()
