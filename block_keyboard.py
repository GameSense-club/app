from collections import namedtuple
import threading
import ctypes
import win32con
import win32api
import win32gui
import atexit
from logging_config import logger

KeyboardEvent = namedtuple('KeyboardEvent', ['event_type', 'key_code',
                                             'scan_code', 'alt_pressed',
                                             'time'])

handlers = []

ctrl = 124554051746
tab = 64424509449
win = 390842024027
f4 = 266287972467
delete = 356482285614

blocked = [ctrl, tab, win, f4, delete]

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
    taskbar(False)
    global running
    if not running:
        logger.debug("Блокировка клавиш запущена")
        listener_thread = threading.Thread(target=listen, daemon=True)
        listener_thread.start()

def stop_block():
    taskbar()
    global running, hook_id
    logger.debug("Блокировка клавиш остановлена")

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

# handlers.append(print_event)

def taskbar(active = True): # скрытие панели задач
    if active == False:
       show = 0
    else: show = 5
    user32 = ctypes.WinDLL('user32')
    hwnd = user32.FindWindowW("Shell_TrayWnd", None)
    if hwnd:
        user32.ShowWindow(hwnd, show)

if __name__ == "__main__":
    blocked = [tab, win, f4, delete]
    start_block()
    input()  # Остановка основного потока