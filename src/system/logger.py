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

    def create_stream_handler(self, level=logging.INFO):
        self.logger.setLevel(level)

        handler = logging.StreamHandler()
        handler.setFormatter(
            colorlog.ColoredFormatter(LOG_FORMAT, log_colors=LEVEL_COLORS)
        )

        return handler
