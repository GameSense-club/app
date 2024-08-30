import webview
import sys
import threading
import socketio
import block_key
from taskbar import taskbar
import number_pc
import notification


sio = socketio.Client()  # Инициализация клиента SocketIO
computer_number = number_pc.get_computer_number()

@sio.event
def connect_client(data):  # Обработка события разблокировки
    print(data)
    if data['message'] == 'unlock':
        taskbar()
        webview.windows[0].minimize()
        block_key.stop()
    elif data['message'] == 'block':
        # webview.windows[0].restore()  # Развернуть окно
        block_key.start()
        taskbar(False)
    
def connect_to_server():  # Подключение к серверу
    sio.connect(f'http://127.0.0.1:100{computer_number}')
    print(f"Подключено к серверу 100{computer_number}")

print(f"Вы ввели номер компьютера: {computer_number}")
threading.Thread(target=connect_to_server).start()  # Фоновый поток для работы WebSocket
client = webview.create_window('GameSense', f'http://127.0.0.1:100{computer_number}', fullscreen=True)
connect_client({"message":"block"})
webview.start()
