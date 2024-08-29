import ctypes
def taskbar(active = True): # скрытие панели задач
    if active == False:
       show = 0
    else: show = 5
    user32 = ctypes.WinDLL('user32')
    hwnd = user32.FindWindowW("Shell_TrayWnd", None)
    if hwnd:
        user32.ShowWindow(hwnd, show)