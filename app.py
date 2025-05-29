import webview
import sys
import requests
import threading
import block_keyboard
from token_utils import *
import logging
import atexit

# Настройка логирования
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

token = create_token()
url = "https://api.game-sense.net/pc "
headers = {"Content-Type": "application/json"}
data = {"token": token}

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
    while True:
        try:
            response = requests.post(url, json=data, headers=headers, timeout=5)
            response.raise_for_status()  # Проверка HTTP-ошибок
            response_data = response.json()

            if response_data["status"] == 'Занят':
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