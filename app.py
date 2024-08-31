import webview
import sys
import threading
import socketio
import block_key
from taskbar import taskbar
import number_pc
import notification
import time

sio = socketio.Client()  # Инициализация клиента SocketIO
computer_number = number_pc.get_computer_number()

@sio.event
def connect():
    print("Успешно подключено к серверу")

@sio.event
def disconnect():
    print("Соединение с сервером потеряно")

@sio.event
def connect_error(data):
    print(f"Ошибка подключения: {data}")

@sio.event
def reconnect():
    print("Повторное подключение к серверу")

@sio.event
def connect_client(data):  # Обработка события разблокировки
    print(f"Проверка: {data}")
    if data['message'] == 'unlock':
        taskbar()
        if webview.windows:
            webview.windows[0].minimize()
        block_key.stop()
    elif data['message'] == 'block':
        if webview.windows:
            webview.windows[0].restore()  # Развернуть окно
        # block_key.start()
        # taskbar(False)
    elif data['message'] == 'notification':
        notification.create_popup("Осталось 5 минут!")

def connect_to_server():  # Подключение к серверу
    while True:
        if not sio.connected:
            try:
                sio.connect(f'http://localhost:100{computer_number}')
                print(f"Подключено к серверу 100{computer_number}")
                sio.wait()  # Ожидание событий
            except Exception as e:
                print(f"Ошибка подключения: {e}")
                time.sleep(5)  # Задержка перед повторной попыткой подключения
        else:
            print("Соединение уже установлено, ожидание событий...")
            sio.wait()

def start_app():
    print(f"Вы ввели номер компьютера: {computer_number}")
    threading.Thread(target=connect_to_server).start()  # Фоновый поток для работы WebSocket
    webview.create_window('GameSense', f'http://localhost:100{computer_number}', fullscreen=True)
    webview.start()

# Запуск приложения в основном потоке
if __name__ == '__main__':
    start_app()
