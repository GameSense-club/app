import webview
import ctypes
import sys
import threading
import socketio
import block_key


sio = socketio.Client() # Инициализация клиента SocketIO

client = None


@sio.event
def minimize(data): # Обработка события сворачивания
    global fullscreen
    fullscreen = False
    print('Получено событие сворачивания:', data['message'])
    taskbar()
    block_key.stop()
    webview.windows[0].minimize()  # Свернуть окно
    
    client_stop(client)
    client_start()

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

def test():
    client_stop()

def client_stop(window):
    window.destroy()

def client_start(fullscreen=True):
    global client
    taskbar()
    if fullscreen:
        client = webview.create_window('GameSense', 'http://127.0.0.1:5000', fullscreen=True)
    else:
        client = webview.create_window('GameSense', 'http://127.0.0.1:5000')

    webview.start()


client_start()
threading.Thread(target=connect_to_server).start() # Фоновый поток для работы WebSocket