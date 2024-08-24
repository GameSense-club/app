from collections import namedtuple
import ctypes
import win32con
import win32api
import win32gui
import atexit
import threading
import time

KeyboardEvent = namedtuple('KeyboardEvent', ['event_type', 'key_code',
                                             'scan_code', 'alt_pressed',
                                             'time'])

handlers = []
blocked = [390842024027, 64424509449, 266287972467]
running = False
hook_id = None

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

def start():
    print("Блокировка клавиш запущена")
    global running
    if not running:
        listener_thread = threading.Thread(target=listen, daemon=True)
        listener_thread.start()

def stop():
    print("Блокировка клавиш остановлена")
    global running
    running = False
    time.sleep(1)  # Give some time for the listener to stop

def print_event(event):
    print("Event:", event)
    print("key_code:", hex(event.key_code))
# handlers.append(print_event)
