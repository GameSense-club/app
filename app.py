import webview
import ctypes
import sys
import threading
import socketio
import block_key


# Инициализация клиента SocketIO
sio = socketio.Client()


# Обработка события сворачивания
@sio.event
def minimize(data):
    print('Получено событие сворачивания:', data['message'])
    taskbar()
    block_key.stop()
    webview.windows[0].minimize()  # Свернуть окно

# Подключение к серверу
def connect_to_server():
    sio.connect('http://127.0.0.1:5000')

# Фоновый поток для работы WebSocket
threading.Thread(target=connect_to_server).start()

# Функция для скрытия панели задач
def taskbar(active = True):
    if active == False:
       show = 0
    else: show = 5
    user32 = ctypes.WinDLL('user32')
    hwnd = user32.FindWindowW("Shell_TrayWnd", None)
    if hwnd:
        user32.ShowWindow(hwnd, show)

# Функция для отображения панели задач
def show_taskbar():
    user32 = ctypes.WinDLL('user32')
    hwnd = user32.FindWindowW("Shell_TrayWnd", None)
    if hwnd:
        user32.ShowWindow(hwnd, 5)
    
taskbar(active=False)
block_key.start()
# Создаем окно с параметром fullscreen
window = webview.create_window('Game Sense', 'http://127.0.0.1:5000', fullscreen=True)

# Запускаем окно с ограничениями
webview.start()
