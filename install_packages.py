import subprocess
import sys
import os

def install_packages(requirements_file):
    if not os.path.exists(requirements_file):
        print(f"Файл {requirements_file} не найден.")
        return

    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_file])
        print("Все библиотеки успешно установлены.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка установки библиотек: {e}")

if __name__ == "__main__":
    requirements_file = 'requirements.txt'
    install_packages(requirements_file)
