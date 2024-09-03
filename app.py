import socket
import threading
import webview
import sys
import tkinter as tk
from tkinter import messagebox
import time
import os
<<<<<<< HEAD
from collections import namedtuple
import ctypes
import win32con
import win32api
import win32gui
import atexit
import ctypes
from PIL import Image, ImageDraw
import pystray


# ---------------------------------------------------------------------------------------------
KeyboardEvent = namedtuple('KeyboardEvent', ['event_type', 'key_code',
                                             'scan_code', 'alt_pressed',
                                             'time'])

handlers = []
blocked = [390842024027, 64424509449, 266287972467]
# , 124554051746
running = False
hook_id = None
stop_event = threading.Event()  # Событие для остановки потока

def listen():
    global running, hook_id

    def low_level_handler(nCode, wParam, lParam):
        event = KeyboardEvent(event_types[wParam], lParam[0], lParam[1],
                              lParam[2] == 32, lParam[3])
        
        if event.key_code in blocked:
            print("Блокировка")
            return -1  # Блокировать обработку сообщения

        for handler in handlers:
            handler(event)

        return ctypes.windll.user32.CallNextHookEx(hook_id, nCode, wParam, lParam)

    event_types = {win32con.WM_KEYDOWN: 'key down',
                   win32con.WM_KEYUP: 'key up',
                   0x104: 'key down',
                   0x105: 'key up',
                   }

    CMPFUNC = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_void_p))
    ctypes.windll.user32.SetWindowsHookExW.argtypes = (
        ctypes.c_int,
        CMPFUNC,
        ctypes.c_void_p,
        ctypes.c_uint
    )
    pointer = CMPFUNC(low_level_handler)

    hook_id = ctypes.windll.user32.SetWindowsHookExW(win32con.WH_KEYBOARD_LL, pointer,
                                                     win32api.GetModuleHandle(None), 0)

    atexit.register(ctypes.windll.user32.UnhookWindowsHookEx, hook_id)

    running = True
    while running:
        msg = win32gui.GetMessage(None, 0, 0)
        win32gui.TranslateMessage(ctypes.byref(msg))
        win32gui.DispatchMessage(ctypes.byref(msg))

        # Проверка события для выхода
        if stop_event.is_set():
            break

def start_block():
    print("Блокировка клавиш запущена")
    global running
    if not running:
        listener_thread = threading.Thread(target=listen, daemon=True)
        listener_thread.start()

def stop_block():
    global running, hook_id
    print("Блокировка клавиш остановлена")

    if running:
        running = False  # Остановить цикл в функции listen
        
        # Установить событие остановки
        stop_event.set()

        if hook_id is not None:
            ctypes.windll.user32.UnhookWindowsHookEx(hook_id)  # Снять хук
            hook_id = None

def print_event(event):
    print("Event:", event)
    print("key_code:", hex(event.key_code))

# handlers.append(print_event)  # Раскомментируйте, если нужно использовать этот обработчик

# ---------------------------------------------------------------------------------------------

def taskbar(active = True): # скрытие панели задач
    if active == False:
       show = 0
    else: show = 5
    user32 = ctypes.WinDLL('user32')
    hwnd = user32.FindWindowW("Shell_TrayWnd", None)
    if hwnd:
        user32.ShowWindow(hwnd, show)

# ---------------------------------------------------------------------------------------------

def create_popup(text):
    # Создаем основное окно
    popup = tk.Tk()
    
    # Устанавливаем стиль окна
    popup.overrideredirect(True)  # Убираем границы и заголовок окна
    popup.wm_attributes("-topmost", True)  # Делаем окно всегда сверху

    # Получаем размеры экрана
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()

    # Устанавливаем размер окна (например, 200x100)
    popup.geometry("260x150+{}+{}".format(screen_width - 260, 0))

    # Добавляем текст в окно
    label = tk.Label(popup, text=text, font=("Poppins", 16), fg="white", bg="#2a1557")
    label.pack(expand=True, fill=tk.BOTH)

    # Скрываем окно через 5 секунд
    popup.after(5000, popup.destroy)

    # Запускаем основной цикл
    popup.mainloop()

# ---------------------------------------------------------------------------------------------
def validate_input(value):
    # Проверка, что введенное значение содержит только цифры или пустую строку
    return value.isdigit() or value == ""

def get_computer_and_server():
    def on_button_click():
        # Действие при нажатии на кнопку
        computer_number = entry_computer.get()
        server_name = entry_server.get()

        if computer_number and server_name:
            root.computer_number = int(computer_number)
            root.server_name = server_name
            root.quit()  # Завершаем главный цикл приложения
        else:
            messagebox.showwarning("Предупреждение", "Пожалуйста, введите номер компьютера и имя сервера.")

    def close_window():
        root.quit()  # Корректно завершаем главный цикл приложения
        root.destroy()  # Полностью закрываем окно

    def center_window(window):
        window.update_idletasks()  # Обновляем информацию о размере окна
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

    # Создаем главное окно
    root = tk.Tk()
    root.title("Введите номер компьютера и сервер")
    root.computer_number = None  # Инициализация переменной для хранения числа
    root.server_name = None  # Инициализация переменной для хранения имени сервера

    # Удаляем рамки окна (если необходимо)
    root.overrideredirect(True)

    # Создаем надпись для номера компьютера
    label_computer = tk.Label(root, text="Введите номер компьютера:")
    label_computer.pack(pady=10)

    # Валидатор для ввода только чисел
    vcmd = (root.register(validate_input), '%P')

    # Создаем поле ввода для номера компьютера
    entry_computer = tk.Entry(root, validate='key', validatecommand=vcmd)
    entry_computer.pack(pady=10)

    # Создаем надпись для сервера
    label_server = tk.Label(root, text="Введите имя сервера:")
    label_server.pack(pady=10)

    # Создаем поле ввода для имени сервера
    entry_server = tk.Entry(root)
    entry_server.pack(pady=10)
    # Задаем значение по умолчанию
    entry_server.insert(0, "192.168.0.103")

    # Создаем кнопку
    button = tk.Button(root, text="Подтвердить", command=on_button_click)
    button.pack(pady=10)

    # Обработчик для закрытия окна
    root.protocol("WM_DELETE_WINDOW", close_window)

    # Центрируем окно на экране
    center_window(root)

    # Запуск главного цикла приложения
    root.mainloop()

    # После выхода из mainloop
    root.destroy()  # Полностью закрываем окно

    return root.computer_number, root.server_name  # Возвращаем введенные значения

# ---------------------------------------------------------------------------------------------


=======
from PIL import Image, ImageDraw
import pystray
>>>>>>> origin/main

# Устанавливаем переменные среды
os.environ['WEBVIEW2_USER_DATA_FOLDER'] = os.path.expanduser('~\\AppData\\Local\\Temp\\WebView2')
computer_number, server_name = get_computer_and_server()
print(server_name)

def get_server_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def start_app():
    global window
    try:
        start_block()
        taskbar(active=False)
        window = webview.create_window('GameSense', f'http://{server_name}:100{computer_number}', fullscreen=True)
        webview.start()
    except Exception as e:
        print(f"Ошибка инициализации WebView: {e}")
        sys.exit(1)

def handle_command(command):
    print(command)
    if command.split("_")[0] == "NOTIFICATION" and command.split("_")[1] == str(computer_number):
        create_popup("Осталось 5 минут!")
        return "Уведомление пришло"
    elif command.split("_")[0] == "BLOCK" and command.split("_")[1] == str(computer_number):
<<<<<<< HEAD
        webview.windows[0].restore()
        start_block()
        taskbar(active=False)
        return "Клиент заблокирован"
    elif command.split("_")[0] == "UNLOCK" and command.split("_")[1] == str(computer_number):
        stop_block()
        window.hide()
        webview.windows[0].minimize()
=======
        window.restore()
        block_key.start()
        taskbar(active=False)
        return "Клиент заблокирован"
    elif command.split("_")[0] == "UNLOCK" and command.split("_")[1] == str(computer_number):
        block_key.stop()
        window.minimize()
>>>>>>> origin/main
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
    # Загрузите изображение и преобразуйте его в формат, который pystray поддерживает
    image = Image.open('logo.jpg')
    return image

def setup_tray_icon():
    # Создаем иконку и запускаем ее
    icon = pystray.Icon('GameSense', create_image(), menu=pystray.Menu(
        pystray.MenuItem('Открыть', on_open),
    ))
    icon.run()

def on_open(icon, item):
    window.show()  # Показываем окно WebView при нажатии на 'Открыть'
    window.restore()

if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    tray_thread = threading.Thread(target=setup_tray_icon)
    tray_thread.daemon = True
    tray_thread.start()

<<<<<<< HEAD
    # Запуск приложения WebView
=======
>>>>>>> origin/main
    start_app()
