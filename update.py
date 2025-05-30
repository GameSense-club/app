import requests
import os
import sys
import zipfile
import shutil
from packaging import version
import logging
import re

APPDATA_DIR = os.getenv('LOCALAPPDATA')
DIR = os.path.join(APPDATA_DIR, "GameSense")
LOG_FILE = os.path.join(DIR, "update.log")

# Создаем папку, если её нет
os.makedirs(DIR, exist_ok=True)


# Настройка логирования
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_latest_tag():
    try:
        # API GitHub для получения тегов
        api_url = "https://api.github.com/repos/GameSense-club/app/tags"
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        
        tags = response.json()
        if not tags:
            return None
            
        # Фильтруем только теги, соответствующие формату v[число] с возможными точками
        version_tags = []
        for tag in tags:
            tag_name = tag.get('name', '')
            if re.match(r'^v\d+(\.\d+)*$', tag_name):
                version_tags.append(tag_name)
        
        if not version_tags:
            return None
            
        # Сортируем по версии и берем последнюю
        version_tags.sort(key=lambda x: version.parse(x), reverse=True)
        return version_tags[0]
        
    except Exception as e:
        logging.error(f"Ошибка при получении тегов: {e}")
        return None

def check_for_updates(current_version):
    latest_tag = get_latest_tag()
    if not latest_tag:
        return None
    
    # Удаляем 'v' из начала тега для сравнения версий
    latest_version = latest_tag[1:] if latest_tag.startswith('v') else latest_tag
    
    if version.parse(latest_version) > version.parse(current_version):
        return latest_version
    return None

def download_and_install_update(latest_version):
    try:
        # URL к MSI файлу на GitHub (используйте raw или release URL)
        msi_url = f"https://github.com/GameSense-club/app/releases/download/v{latest_version}/GameSense-{latest_version}-win64.msi"
        
        # Временная папка для загрузки
        temp_dir = os.path.join(os.environ['TEMP'], 'GameSenseUpdate')
        os.makedirs(temp_dir, exist_ok=True)
        
        # Скачиваем MSI
        msi_path = os.path.join(temp_dir, f"GameSense_{latest_version}.msi")
        with requests.get(msi_url, stream=True) as r:
            r.raise_for_status()
            with open(msi_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        # Запускаем установщик (MSI)
        os.startfile(msi_path)
        sys.exit(0)  # Закрываем текущее приложение
        
    except Exception as e:
        logging.error(f"Ошибка при установке обновления: {e}")