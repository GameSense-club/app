import keyboard
import win32gui
import win32con


def set_always_on_top(hwnd):
    win32gui.SetWindowPos(
        hwnd,
        win32con.HWND_TOPMOST,  # Поместить поверх всех окон
        0, 0, 0, 0,
        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
    )

    

def hide_in_bar(hwnd):
    # Устанавливаем стиль TOOLWINDOW и NOACTIVATE
    new_style = (
        win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        | win32con.WS_EX_TOOLWINDOW
        | win32con.WS_EX_NOACTIVATE
    )
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_style)

def show_in_bar(hwnd):
    # Убираем стили TOOLWINDOW и NOACTIVATE
    new_style = (
        win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        & ~win32con.WS_EX_TOOLWINDOW
        & ~win32con.WS_EX_NOACTIVATE
    )
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_style)
    
    # Принудительно активируем окно (если нужно)
    try:
        win32gui.SetForegroundWindow(hwnd)
    except:
        logger.error("Ошибка установки оверлея")
    # Обновляем окно (если изменения не применяются)
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
    win32gui.UpdateWindow(hwnd)

def show_window(full=False):
    global WINDOW_SHOW
    if not window:
        return

    hwnd = win32gui.FindWindow(None, "GameSense")
    if hwnd:
        set_always_on_top(hwnd)
        
    screens = webview.screens
    if not screens:
        return
        
    main_screen = screens[0]
    screen_width = main_screen.width
    screen_height = main_screen.height

    if full == False and ACTIVE == True:
        screen_width = 600
        window.resize(screen_width, screen_height)
    
        if WINDOW_SHOW == False:
            WINDOW_SHOW = True
            window.show()
            hwnd = win32gui.FindWindow(None, "GameSense")
            hide_in_bar(hwnd)
        else:
            WINDOW_SHOW = False
            window.hide()

    else:
        window.resize(screen_width, screen_height)
        window.show()
        hwnd = win32gui.FindWindow(None, "GameSense")
        show_in_bar(hwnd)