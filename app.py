import webview
import ctypes
import sys

# Функция для скрытия панели задач
def taskbar(active = True):
    if active == False:
       show = 0
    else: show = 5
    user32 = ctypes.WinDLL('user32')
    hwnd = user32.FindWindowW("Shell_TrayWnd", None)
    if hwnd:
        user32.ShowWindow(hwnd, show)  # SW_HIDE = 0

# Функция для отображения панели задач
def show_taskbar():
    user32 = ctypes.WinDLL('user32')
    hwnd = user32.FindWindowW("Shell_TrayWnd", None)
    if hwnd:
        user32.ShowWindow(hwnd, 5)  # SW_SHOW = 5

# Проверка, что приложение запущено на Windows
if sys.platform == 'win32':
    taskbar(False)

# Создаем окно с параметром fullscreen
window = webview.create_window('My Web App', 'http://localhost:5000', fullscreen=True)

# Запускаем окно с ограничениями
webview.start()

# Восстанавливаем панель задач после закрытия окна
if sys.platform == 'win32':
    taskbar()
