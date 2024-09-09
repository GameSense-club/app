# библиотеки приложения
import socket
import threading
import webview
import sys
import tkinter as tk
from tkinter import messagebox
import time
import os
from collections import namedtuple
import ctypes
import win32con
import win32api
import win32gui
import atexit
import ctypes
from PIL import Image, ImageDraw
import pystray

import os
import requests
import logging
from github import Github
from zipfile import ZipFile
import io
import subprocess

# Параметры
username = "Falbue"
token = "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"
REPO = "GameSense-App"
REPO_URL = f"https://{username}:{token}@github.com/{username}/{REPO}"
REPO_PATH = f"/{REPO}"  # Локальная папка для хранения репозитория
RUN_FILE = "app.py"  # Файл, который нужно запускать
LOG_FILE = "error_log.txt"  # Файл для логирования ошибок

# Настройка логирования
logging.basicConfig(filename=LOG_FILE, level=logging.ERROR, format='%(asctime)s - %(message)s')

def download_repo_as_zip(repo_url, repo_path):
    """Скачивает репозиторий как zip и распаковывает его."""
    if not os.path.exists(repo_path):
        try:
            # Запрос на скачивание архива репозитория
            response = requests.get(f"{repo_url}/archive/refs/heads/main.zip", stream=True)
            if response.status_code == 200:
                # Распаковка архива
                with ZipFile(io.BytesIO(response.content)) as zip_ref:
                    zip_ref.extractall(repo_path)
                print(f"Репозиторий скачан и распакован в {repo_path}")
            else:
                logging.error(f"Ошибка при скачивании репозитория: {response.status_code}")
                return False
        except Exception as e:
            logging.error(f"Ошибка при скачивании репозитория: {e}")
            return False
    return True

def run_script(file_path):
    """Запускает файл и логирует ошибку в случае её появления."""
    try:
        subprocess.run(['python', file_path], check=True)
        print(f"Скрипт {file_path} выполнен успешно.")
    except subprocess.CalledProcessError as e:
        error_message = f"Ошибка при выполнении {file_path}: {e}"
        logging.error(error_message)
        print(error_message)

def main():
    # Проверяем и скачиваем репозиторий как zip
    if download_repo_as_zip(REPO_URL, REPO_PATH):
        # Путь к запускаемому файлу
        file_to_run = os.path.join(REPO_PATH, REPO, "main", RUN_FILE)
        # Запуск скрипта
        run_script(file_to_run)

if __name__ == "__main__":
    main()
