import webview
import sys
import requests
import threading
import block_keyboard
from token_utils import *

token = create_token()

window = None  # Объявляем window глобально

def start_app():
    global window
    try:
        window = webview.create_window('GameSense', 'https://game-sense.net ', fullscreen=True)
        webview.start()
    except Exception as e:
        print(f"Ошибка инициализации WebView: {e}")
        sys.exit(1)

def send_post():
    while True:
        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()
        # print(response_data["status"])
        
        if response_data["status"] == 'Активен':
            if window is not None:
                window.hide()
                block_keyboard.stop_block()
        else:
            if window is not None:
                window.show()
                webview.windows[0].restore()
                block_keyboard.start_block()
        
        import time
        time.sleep(1)

thread = threading.Thread(target=send_post, daemon=True)
thread.start()

start_app()