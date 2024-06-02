from abc import ABC, abstractmethod
import logging

import colorlog

LOG_FORMAT = "%(log_color)s[%(levelname)s] %(asctime)s%(reset)s | %(message)s"

LEVEL_COLORS = {
    "DEBUG": "cyan",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "white,bg_red",
}

# Adapted from the stdlib
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0

LOG_LEVEL = {
    "CRITICAL": CRITICAL,
    "FATAL": FATAL,
    "ERROR": ERROR,
    "WARNING": WARNING,
    "WARN": WARN,
    "INFO": INFO,
    "DEBUG": DEBUG,
    "NOTSET": NOTSET,
}


class LoggerInterface(ABC):
    @abstractmethod
    def configure_logger(self):
        """
        Configure the logger to use Structlog based on a configuration file or environment variables.
        """
        pass

    @abstractmethod
    def critical(self, message, **kwargs):
        pass

    @abstractmethod
    def error(self, message, **kwargs):
        pass

    @abstractmethod
    def warning(self, message, **kwargs):
        pass

    @abstractmethod
    def info(self, message, **kwargs):
        pass

    @abstractmethod
    def debug(self, message, **kwargs):
        pass

    def get_log_level(self, level: str):
        return LOG_LEVEL.get(level)

    def create_stream_handler(self, level=logging.INFO):
        self.logger.setLevel(level)

        handler = logging.StreamHandler()
        handler.setFormatter(
            colorlog.ColoredFormatter(LOG_FORMAT, log_colors=LEVEL_COLORS)
        )

        return handler
