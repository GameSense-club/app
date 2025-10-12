import requests
import os
import sys
import zipfile
import shutil
from packaging import version
import logging
import re
import subprocess
import time

APPDATA_DIR = os.getenv('LOCALAPPDATA')
DIR = os.path.join(APPDATA_DIR, "GameSense")
LOG_FILE = os.path.join(DIR, "update.log")

os.makedirs(DIR, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_latest_tag():
    try:
        api_url = "https://api.github.com/repos/GameSense-club/app/tags"
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        
        tags = response.json()
        if not tags:
            return None
            
        version_tags = []
        for tag in tags:
            tag_name = tag.get('name', '')
            if re.match(r'^v\d+(\.\d+)*$', tag_name):
                version_tags.append(tag_name)
        
        if not version_tags:
            return None

        version_tags.sort(key=lambda x: version.parse(x), reverse=True)
        return version_tags[0]
        
    except Exception as e:
        logging.error(f"Ошибка при получении тегов: {e}")
        return None

def check_for_updates(current_version):
    latest_tag = get_latest_tag()
    if not latest_tag:
        return None

    latest_version = latest_tag[1:] if latest_tag.startswith('v') else latest_tag
    
    if version.parse(latest_version) > version.parse(current_version):
        return latest_version
    return None

def download_and_install_update(latest_version):
    try:
        msi_url = f"https://github.com/GameSense-club/app/releases/download/v{latest_version}/GameSense-{latest_version}-win64.msi"
        temp_dir = os.path.join(os.environ['TEMP'], 'GameSenseUpdate')
        os.makedirs(temp_dir, exist_ok=True)
        
        msi_path = os.path.join(temp_dir, f"GameSense_{latest_version}.msi")
        with requests.get(msi_url, stream=True) as r:
            r.raise_for_status()
            with open(msi_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        logging.info(f"Загрузка завершена: {msi_path}")
        
        # Автоматическая установка с флагами для тихой установки
        cmd = [
            'msiexec',
            '/i',  # install
            msi_path,
            '/quiet',  # quiet installation
            '/norestart',  # no restart
            '/qn'  # no UI
        ]
        
        logging.info("Начинаю автоматическую установку...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            logging.info("Установка прошла успешно")
            print("Установка завершена успешно!")
        else:
            logging.error(f"Ошибка установки: {result.stderr}")
            print(f"Ошибка установки: {result.stderr}")
        
        # Удаляем временный файл
        try:
            os.remove(msi_path)
            os.rmdir(temp_dir)
        except:
            pass
            
        sys.exit(0)
        
    except Exception as e:
        logging.error(f"Ошибка при установке обновления: {e}")
        print(f"Ошибка: {e}")

# Пример использования
if __name__ == "__main__":
    # Укажите текущую версию вашей программы
    current_version = "1.0.0"  # Замените на актуальную версию
    
    latest_version = check_for_updates(current_version)
    if latest_version:
        print(f"Найдено обновление: v{latest_version}")
        download_and_install_update(latest_version)
    else:
        print("Обновлений нет")