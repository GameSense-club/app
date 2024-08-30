import webview
import sys
import threading
import socketio
import block_key
from taskbar import taskbar
import number_pc


sio = socketio.Client()  # Инициализация клиента SocketIO
computer_number = number_pc.get_computer_number()

@sio.event
def minimize(data):  # Обработка события сворачивания
    print('Получено событие сворачивания:', data['message'])
    webview.windows[0].minimize()  # Свернуть окно

@sio.event
def unlock(data):  # Обработка события разблокировки
    print('Получено событие:', data['message'])
    taskbar()
    webview.windows[0].minimize()
    block_key.stop()

@sio.event
def block(data):  # Обработка события блокировки
    print('Получено событие:', data['message'])
    webview.windows[0].restore()  # Развернуть окно
    block_key.start()
    taskbar(active=False)

def connect_to_server():  # Подключение к серверу
    sio.connect(f'http://127.0.0.1:100{computer_number}')

print(f"Вы ввели номер компьютера: {computer_number}")
threading.Thread(target=connect_to_server).start()  # Фоновый поток для работы WebSocket
client = webview.create_window('GameSense', f'http://127.0.0.1:100{computer_number}', fullscreen=True)
# block("Ручная блокировка")
block_key.start()
taskbar(active=True)
webview.start()
