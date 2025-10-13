VERSION="1.0.4"

import webview
import sys
import threading
import atexit
from datetime import datetime, timedelta, timezone

import subprocess
import os

from utils import block_keyboard
from utils.token import *
from utils.update import *
from utils import autostart
from utils import logger
from utils.tray import *



try: 
    import config
    DEBUG = config.DEBUG
    logger = logger.setup(True, "APP", "data/")
    HOST = "http://127.0.0.1:5000"
except: 
    DEBUG = False
    logger = logger.setup(False, "APP", "data/")
    HOST = "https://pc.game-sense.ru"

logger.info(f"Версия: {VERSION}")
autostart.autostart()

if DEBUG == False:
    APPDATA_DIR = os.getenv('LOCALAPPDATA')
    DIR = os.path.join(APPDATA_DIR, "GameSense")
else:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    DIR = os.path.join(script_dir, "data")
    
token = create_token(DIR)
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
window = None
ACTIVE = False
WINDOW_SHOW = False


def get_ntp_time():
    return # Нужно доделать

# 89951941908 Дидар

def edit_status():
    url = "https://api.game-sense.ru/pc/status"
    data = {"token":token, "status":"активен"}
    response = requests.post(url, json=data, headers=headers, timeout=5)


def start_app():
    global window
    version = check_for_updates(VERSION)
    if version:
        download_and_install_update(version)
    try:
        logger.info("Инициализация WebView")
        window = webview.create_window('GameSense', f'{HOST}/login_pc/{token}', fullscreen=True)
        keyboard.add_hotkey('alt+x', show_window)
        webview.start()
    except Exception as e:
        logger.error(f"Ошибка инициализации WebView: {e}", exc_info=True)
        sys.exit(1)

def send_post():
    global ACTIVE
    import requests
    while True:
        try:
            url = "https://api.game-sense.ru/pc"
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()  # Проверка HTTP-ошибок
            response_data = response.json()

            if response_data["status"] == 'занят':
                time = response_data["time_active"]
                time_zone = int(response_data["time_zone"])
                
                if time:
                    time_active = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
                    time_active += timedelta(hours=time_zone)
                    now_time = get_ntp_time()
                    now_time = datetime.strptime(now_time, "%Y-%m-%d %H:%M:%S")
                    now_time += timedelta(hours=time_zone)
                    if now_time > time_active:
                        edit_status()
                else:
                    edit_status()
                    

                if window is not None and ACTIVE == False:
                    ACTIVE = True
                    window.hide()
                    block_keyboard.stop_block()

            elif response_data["status"] == 'ремонт':
                if window is not None and ACTIVE == False:
                    ACTIVE = True
                    window.hide()
                    block_keyboard.stop_block()

            else:
                if window is not None:
                    ACTIVE = False
                    if DEBUG == False:
                        show_window(True, window)
                        block_keyboard.start_block()


        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка сети: {e}", exc_info=True)
        except KeyError:
            logger.error("Неверный формат ответа от сервера (отсутствует 'status')")
        except Exception as e:
            logger.error(f"Неизвестная ошибка: {e}", exc_info=True)

        import time
        time.sleep(5)

def exit_handler():
    logger.info("Приложение завершает работу")
    block_keyboard.stop_block()

atexit.register(exit_handler)

thread = threading.Thread(target=send_post, daemon=True)
thread.start()

start_app()
