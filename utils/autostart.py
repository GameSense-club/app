import winreg
import sys
import os
from . import logger

try: 
    import config
    DEBUG = config.DEBUG
    logger = logger.setup(True, "AUTOSTART", "data/")
except: 
    DEBUG = False
    logger = logger.setup(False, "APP", "data/")

def autostart():
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        app_name = "GameSense"
        # Путь к исполняемому файлу после установки
        exe_path = os.path.join(os.path.dirname(sys.executable), "GameSense.exe")
        
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, exe_path)
    except Exception as e:
        logger.error(f"Не удалось установить на автозапуск: {str(e)}")