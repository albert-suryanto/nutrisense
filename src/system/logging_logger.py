import logging
from src.system.logger import LoggerInterface


class LoggingLogger(LoggerInterface):
    def __init__(self, logger_name=None, logging_level=logging.INFO):
        self.logger = logging.getLogger(logger_name or __name__)
        self.configure_logger(logging_level)

    def configure_logger(self, level=logging.INFO):
        handler = self.create_stream_handler(level)
        self.logger.addHandler(handler)

    def critical(self, message, **kwargs):
        self.logger.critical(message, **kwargs)

    def error(self, message, **kwargs):
        self.logger.error(message, **kwargs)

    def warning(self, message, **kwargs):
        self.logger.warning(message, **kwargs)

    def info(self, message, **kwargs):
        self.logger.info(message, **kwargs)

    def debug(self, message, **kwargs):
        self.logger.debug(message, **kwargs)
