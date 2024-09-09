import subprocess
import sys
import os
import ctypes

def hide_console():
    """Скрывает консольное окно."""
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def run_script(script_name):
    """Запускает указанный скрипт."""
    try:
        print(f"Запуск {script_name}...")
        subprocess.check_call([sys.executable, script_name])
        print(f"{script_name} успешно завершен.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении {script_name}: {e}")

if __name__ == "__main__":
    # Скрываем консольное окно
    hide_console()

    # Скрипты для запуска
    scripts_to_run = ['update.py', 'install_packages.py', 'app.py']
    
    for script in scripts_to_run:
        run_script(script)

    # Скрытие консоли должно произойти до запуска app.py, чтобы она не отображалась
    # Примечание: вы можете также использовать subprocess с параметрами для полной скрытности
