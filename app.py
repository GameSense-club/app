import webview
import sys
import threading
import block_keyboard
from token_utils import *
import logging
import atexit
from datetime import datetime, timedelta
import add_autostart

add_autostart.add_to_autostart()

def edit_status():
    url = "https://api.game-sense.net/pc/status"
    data = {"token":token, "status":"активен"}
    response = requests.post(url, json=data, headers=headers, timeout=5)

# Настройка логирования
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

token = create_token()
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

window = None  # Объявляем window глобально

def start_app():
    global window
    try:
        logging.info("Инициализация WebView")
        window = webview.create_window('GameSense', 'https://game-sense.net ', fullscreen=True)
        webview.start()
    except Exception as e:
        logging.error(f"Ошибка инициализации WebView: {e}", exc_info=True)
        print(f"Ошибка инициализации WebView: {e}")
        sys.exit(1)

def send_post():
    import requests
    while True:
        try:
            url = "https://api.game-sense.net/pc"
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()  # Проверка HTTP-ошибок
            response_data = response.json()

            if response_data["status"] == 'занят':
                time = response_data["time_active"]
                
                if time:
                    time_active = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
                    time_active += timedelta(hours=5)
                    print(time_active)
                    now_time = datetime.now()

                    if now_time > time_active:
                        edit_status()
                else:
                    edit_status()
                    

                if window is not None:
                    window.hide()
                    block_keyboard.stop_block()
            else:
                if window is not None:
                    window.show()
                    block_keyboard.start_block()


        except requests.exceptions.RequestException as e:
            logging.error(f"Ошибка сети: {e}", exc_info=True)
            print(f"Ошибка сети: {e}")
        except KeyError:
            logging.error("Неверный формат ответа от сервера (отсутствует 'status')")
        except Exception as e:
            logging.error(f"Неизвестная ошибка: {e}", exc_info=True)

        import time
        time.sleep(1)

def exit_handler():
    logging.info("Приложение завершает работу")
    block_keyboard.stop_block()

atexit.register(exit_handler)

thread = threading.Thread(target=send_post, daemon=True)
thread.start()

start_app()