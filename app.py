VERSION="1.0.1.7.1.2"

import webview
import sys
import threading
import block_keyboard
from token_utils import *
import logging
import atexit
from datetime import datetime, timedelta
import add_autostart
import keyboard
import win32gui
import win32con
import ntplib
from update import *

add_autostart.add_to_autostart()

APPDATA_DIR = os.getenv('LOCALAPPDATA')
DIR = os.path.join(APPDATA_DIR, "GameSense")
LOG_FILE = os.path.join(DIR, "app.log")
token = create_token()
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
window = None
ACTIVE = False
WINDOW_SHOW = False

# Создаем папку, если её нет
os.makedirs(DIR, exist_ok=True)


# Настройка логирования
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_ntp_time():
    ntp_client = ntplib.NTPClient()
    response = ntp_client.request("pool.ntp.org")
    utc_time = datetime.fromtimestamp(response.tx_time, timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    return utc_time


def edit_status():
    url = "https://api.game-sense.net/pc/status"
    data = {"token":token, "status":"активен"}
    response = requests.post(url, json=data, headers=headers, timeout=5)

def set_always_on_top(hwnd):
    win32gui.SetWindowPos(
        hwnd,
        win32con.HWND_TOPMOST,  # Поместить поверх всех окон
        0, 0, 0, 0,
        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
    )

    

def hide_in_bar(hwnd):
    # Устанавливаем стиль TOOLWINDOW и NOACTIVATE
    new_style = (
        win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        | win32con.WS_EX_TOOLWINDOW
        | win32con.WS_EX_NOACTIVATE
    )
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_style)

def show_in_bar(hwnd):
    # Убираем стили TOOLWINDOW и NOACTIVATE
    new_style = (
        win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        & ~win32con.WS_EX_TOOLWINDOW
        & ~win32con.WS_EX_NOACTIVATE
    )
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_style)
    
    # Принудительно активируем окно (если нужно)
    win32gui.SetForegroundWindow(hwnd)
    
    # Обновляем окно (если изменения не применяются)
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
    win32gui.UpdateWindow(hwnd)

def show_window(full=False):
    global WINDOW_SHOW
    if not window:
        return

    hwnd = win32gui.FindWindow(None, "GameSense")
    if hwnd:
        set_always_on_top(hwnd)
        
    screens = webview.screens
    if not screens:
        return
        
    main_screen = screens[0]
    screen_width = main_screen.width
    screen_height = main_screen.height

    if full == False and ACTIVE == True:
        screen_width = 600
        window.resize(screen_width, screen_height)
    
        if WINDOW_SHOW == False:
            WINDOW_SHOW = True
            window.show()
            hwnd = win32gui.FindWindow(None, "GameSense")
            hide_in_bar(hwnd)
        else:
            WINDOW_SHOW = False
            window.hide()

    else:
        window.resize(screen_width, screen_height)
        window.show()
        hwnd = win32gui.FindWindow(None, "GameSense")
        show_in_bar(hwnd)


def start_app():
    global window
    version = check_for_updates(VERSION)
    if version:
        download_and_install_update(version)
    try:
        logging.info("Инициализация WebView")
        window = webview.create_window('GameSense', f'https://game-sense.net/login_pc/{token}', fullscreen=True)
        keyboard.add_hotkey('alt+x', show_window)
        webview.start()
    except Exception as e:
        logging.error(f"Ошибка инициализации WebView: {e}", exc_info=True)
        print(f"Ошибка инициализации WebView: {e}")
        sys.exit(1)

def send_post():
    global ACTIVE
    import requests
    while True:
        try:
            url = "https://api.game-sense.net/pc"
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
                    now_time += timedelta(hours=time_zone)

                    if now_time > time_active:
                        edit_status()
                else:
                    edit_status()
                    

                if window is not None and ACTIVE == False:
                    ACTIVE = True
                    window.hide()
                    block_keyboard.stop_block()
            else:
                if window is not None:
                    ACTIVE = False
                    show_window(True)
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