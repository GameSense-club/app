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
from PIL import Image, ImageDraw
import pystray

# Устанавливаем переменные среды
os.environ['WEBVIEW2_USER_DATA_FOLDER'] = os.path.expanduser('~\\AppData\\Local\\Temp\\WebView2')
computer_number, server_name = number_pc.get_computer_and_server()
print(server_name)

def get_server_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def start_app():
    global window
    try:
        block_key.start()
        taskbar(active=False)
        window = webview.create_window('GameSense', f'http://{server_name}:100{computer_number}', fullscreen=True)
        webview.start()
    except Exception as e:
        print(f"Ошибка инициализации WebView: {e}")
        sys.exit(1)

def handle_command(command):
    print(command)
    if command.split("_")[0] == "NOTIFICATION" and command.split("_")[1] == str(computer_number):
        notification.create_popup("Осталось 5 минут!")
        return "Уведомление пришло"
    elif command.split("_")[0] == "BLOCK" and command.split("_")[1] == str(computer_number):
        window.restore()
        block_key.start()
        taskbar(active=False)
        return "Клиент заблокирован"
    elif command.split("_")[0] == "UNLOCK" and command.split("_")[1] == str(computer_number):
        block_key.stop()
        window.minimize()
        taskbar()
        window.hide()
        return "Клиент разблокирован"
    else:
        return f"Неизвестная команда: {command}"

def run_server(host='0.0.0.0', port=65432):
    ip_address = get_server_address()
    print(f"Сервер запущен {ip_address}:{port}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Сервер слушает {host}:{port}")

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

def create_image():
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), color=(0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle(
        (width//4, height//4, width//4*3, height//4*3),
        fill=(255, 255, 255)
    )
    return image

def on_open(icon, item):
    window.show()  # Показываем окно WebView при нажатии на 'Открыть'
    window.restore()

def setup_tray_icon():
    icon = pystray.Icon('test_icon', create_image(), menu=pystray.Menu(
        pystray.MenuItem('Открыть', on_open),
    ))
    icon.run()

if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    tray_thread = threading.Thread(target=setup_tray_icon)
    tray_thread.daemon = True
    tray_thread.start()

    start_app()
