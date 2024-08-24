import webview
import ctypes
import sys
import threading
import socketio
import block_key


sio = socketio.Client() # Инициализация клиента SocketIO


@sio.event
def minimize(data): # Обработка события сворачивания
    print('Получено событие сворачивания:', data['message'])
    taskbar()
    block_key.stop()
    webview.windows[0].minimize()  # Свернуть окно

def connect_to_server(): # Подключение к серверу
    sio.connect('http://127.0.0.1:5000')

def taskbar(active = True): # скрытие панели задач
    if active == False:
       show = 0
    else: show = 5
    user32 = ctypes.WinDLL('user32')
    hwnd = user32.FindWindowW("Shell_TrayWnd", None)
    if hwnd:
        user32.ShowWindow(hwnd, show)
    

window = webview.create_window('Game Sense', 'http://127.0.0.1:5000', fullscreen=True)
taskbar(active=False)
block_key.start()

threading.Thread(target=connect_to_server).start() # Фоновый поток для работы WebSocket

webview.start()
