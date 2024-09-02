import socket
import threading
import webview
import sys
import block_key
from taskbar import taskbar
import number_pc
import notification
import time
import os

os.environ['WEBVIEW2_USER_DATA_FOLDER'] = os.path.expanduser('~\\AppData\\Local\\Temp\\WebView2')
computer_number, server_name = number_pc.get_computer_and_server()
print(server_name)

def start_app():
    try:
        # Создание окна
        webview.create_window('GameSense', f'http://88.206.10.174:100{computer_number}', fullscreen=True)
        webview.start()
    except Exception as e:
        print(f"Ошибка инициализации WebView: {e}")
        sys.exit(1)  # Завершение программы при возникновении ошибки

def get_server_address():
    # Получаем имя хоста
    hostname = socket.gethostname()
    # Получаем IP-адрес
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def handle_command(command):
    if command == "NOTIFICATION":
        notification.create_popup("Осталось 5 минут!")
        return "Уведомление пришло"
    elif command == "BLOCK":
        webview.windows[0].restore()
        return "Клиент заблокирован"
    elif command == "UNLOCK":
        webview.windows[0].minimize()
        return "Окно разблокировано"
    else:
        return "Unknown command."

def run_server(host='0.0.0.0', port=65432):
    ip_address = get_server_address()
    print(f"Server will be available at {ip_address}:{port}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    command = data.decode('utf-8').strip()
                    response = handle_command(command)
                    conn.sendall(response.encode('utf-8'))

if __name__ == "__main__":
    # Создаем поток для сервера
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # Запуск приложения WebView
    start_app()
