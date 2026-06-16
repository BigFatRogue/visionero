import logging
import traceback
from datetime import datetime
from colorama import init, Fore

init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA + Fore.LIGHTWHITE_EX,
    }

    def format(self, record):
        log_message = super().format(record)
        color = self.COLORS.get(record.levelno)
        if color:
            return f"{color}{log_message}"
        return log_message

formatter = ColoredFormatter('%(levelname)s:\t %(asctime)s - [%(filename)s:%(lineno)d] - %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

error_file_handler = logging.FileHandler("errors.log", encoding="utf-8")
error_file_handler.setLevel(logging.ERROR)
error_file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger.addHandler(error_file_handler)
logger.addHandler(console_handler)


class Metrics:
    def __init__(self):
        self.last_error: str | None = None
        self.last_error_time: datetime | None = None
        self.count_error = 0
    
    def log_error(self, message: str, error: Exception, has_print=True, has_write=True):
        self.last_error = str(error)
        self.last_error_time = datetime.now()
        self.count_error += 1
        
        if has_print:
            logger.error(f'{message} - {error}')
        if has_write:
            logger.error(traceback.format_exc())

    def log_info(self, message: str):
        logger.info(message)

    def get_statistics(self) -> dict:
        return {
            'last_error': self.last_error,
            'count_error': self.count_error,
            'last_error_time': self.last_error_time
        }

metrics = Metrics()