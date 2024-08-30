import webview
import sys
import threading
import socketio
import block_key
from taskbar import taskbar
import number_pc


sio = socketio.Client() # Инициализация клиента SocketIO


@sio.event
def minimize(data): # Обработка события сворачивания
    print('Получено событие сворачивания:', data['message'])
    webview.windows[0].minimize()  # Свернуть окно

@sio.event
def unlock(data): # Обработка события сворачивания
    print('Получено событие:', data['message'])
    taskbar()
    webview.windows[0].minimize()
    # block_key.stop()

def connect_to_server(): # Подключение к серверу
    sio.connect('http://127.0.0.1:5000')


computer_number = number_pc.get_computer_number()
print(f"Вы ввели номер компьютера: {computer_number}")
threading.Thread(target=connect_to_server).start() # Фоновый поток для работы WebSocket
client = webview.create_window('GameSense', 'http://127.0.0.1:5000', fullscreen=True)
# taskbar(active = False)
taskbar()
webview.start()