import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import os

class CustomFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_log_date = None

    def format(self, record):
        current_log_date = datetime.utcfromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')
        
        # Ellenőrzi, hogy a mostani és az előző log dátuma megegyezik-e másodpercre pontosan
        if self.last_log_date is not None and current_log_date == self.last_log_date:
            # Ha igen, nem tesz hozzá üres sort az üzenet elé
            formatted_message = super().format(record)
        else:
            # Ha nem, hozzáad üres sort az üzenet elé és frissíti az utolsó log dátumát
            formatted_message = f"\n{super().format(record)}"
            self.last_log_date = current_log_date

        return formatted_message

def setup_logger():
    # Az aktuális dátum formázása
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Logs mappa létrehozása, ha még nem létezik
    logs_folder = "logs"
    os.makedirs(logs_folder, exist_ok=True)

    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)

    # Konzolra kiíratás beállítása
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(formatter)

    # Fájlba kiíratás beállítása a mai dátummal a logs mappában
    file_handler = TimedRotatingFileHandler(
        os.path.join(logs_folder, f'bot_{current_date}.log'),
        when='midnight',  # naponta egy új fájl
        encoding='utf-8',
        delay=True
    )
    file_handler.setLevel(logging.INFO)

    # A saját formázót használja
    custom_formatter = CustomFormatter(fmt='[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(custom_formatter)

    # Handler-ek hozzáadása a loggerhez
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
