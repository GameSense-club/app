import webview
import sys
import threading
import socketio
import block_key
from taskbar import taskbar


sio = socketio.Client() # Инициализация клиента SocketIO


@sio.event
def minimize(data): # Обработка события сворачивания
    print('Получено событие сворачивания:', data['message'])
    taskbar()
    webview.windows[0].minimize()  # Свернуть окно
    # block_key.stop()

def connect_to_server(): # Подключение к серверу
    sio.connect('http://127.0.0.1:5000')


threading.Thread(target=connect_to_server).start() # Фоновый поток для работы WebSocket
client = webview.create_window('GameSense', 'http://127.0.0.1:5000', fullscreen=True)
taskbar(active = False)
webview.start()