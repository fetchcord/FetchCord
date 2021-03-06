import sys
import logging
from logging.handlers import TimedRotatingFileHandler

class Logger(logging.Logger):
    FORMATTER = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    file: str
    console_handler: logging.StreamHandler
    file_handler: TimedRotatingFileHandler

    def get_console_handler() -> logging.StreamHandler:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(Logger.FORMATTER)

        return console_handler

    def get_file_handler(file: str) -> TimedRotatingFileHandler:
        file_handler = TimedRotatingFileHandler(file, when="midnight")
        file_handler.setFormatter(Logger.FORMATTER)

        return file_handler

    def __init__(self, file: str, name: str, level: int = logging.INFO):
        super().__init__(logging.getLogger(name))

        self.file = file
        self.console_handler = Logger.get_console_handler()
        self.file_handler = Logger.get_file_handler(file)

        self.setLevel(level)
        self.addHandler(self.console_handler)
        self.addHandler(self.file_handler)

        self.propagate = False