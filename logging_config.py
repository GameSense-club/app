import logging
import sys
from pathlib import Path
import os

try: 
    import config
    DEBUG = config.DEBUG
except: DEBUG = False


if DEBUG:
    DIR = "lib"
else:
    APPDATA_DIR = os.getenv('LOCALAPPDATA')
    DIR = os.path.join(APPDATA_DIR, "GameSense")

LOG_FILE = os.path.join(DIR, "app.log")

def setup_logging():
    """Настройка логирования для приложения"""
    
    # Создаем логгер
    logger = logging.getLogger()
    
    # Удаляем все существующие обработчики
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Уровень логирования
    log_level = logging.INFO if DEBUG else logging.DEBUG
    logger.setLevel(log_level)
    
    # Форматтер
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # Обработчик для вывода в консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Если не DEBUG, добавляем файловый обработчик
    if not DEBUG:
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

# Инициализируем логгер при импорте модуля
logger = setup_logging()