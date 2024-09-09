import os
import subprocess
import git
import logging
from datetime import datetime
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

# Параметры
REPO = "GameSense-App"
REPO_URL = f"https://github.com/Falbue/{REPO}"  # URL закрытого репозитория
REPO_PATH = f"/{REPO}"  # Локальная папка для хранения репозитория
RUN_FILE = "app.py"  # Файл, который нужно запускать
LOG_FILE = "error_log.txt"  # Файл для логирования ошибок

# Настройка логирования
logging.basicConfig(filename=LOG_FILE, level=logging.ERROR, 
                    format='%(asctime)s - %(message)s')

def clone_or_update_repo(repo_url, repo_path):
    """Клонирует или обновляет репозиторий."""
    if not os.path.exists(repo_path):
        try:
            # Клонирование репозитория
            git.Repo.clone_from(repo_url, repo_path)
            print(f"Репозиторий склонирован в {repo_path}")
        except Exception as e:
            logging.error(f"Ошибка при клонировании репозитория: {e}")
            return False
    else:
        try:
            # Обновление репозитория
            repo = git.Repo(repo_path)
            repo.remotes.origin.pull()
            print(f"Репозиторий обновлен в {repo_path}")
        except Exception as e:
            logging.error(f"Ошибка при обновлении репозитория: {e}")
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
    # Проверяем и обновляем репозиторий
    if clone_or_update_repo(REPO_URL, REPO_PATH):
        # Путь к запускаемому файлу
        file_to_run = os.path.join(REPO_PATH, RUN_FILE)
        # Запуск скрипта
        run_script(file_to_run)

if __name__ == "__main__":
    main()
