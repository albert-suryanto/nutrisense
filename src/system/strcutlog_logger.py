import structlog
from typing import Dict, Any
import src.system.logger as logger
from src.system.logger import LoggerInterface


class StructLogLogger(LoggerInterface):
    def __init__(self, logger_name=None, logging_level=logger.INFO):
        self.logger = structlog.getLogger(logger_name or __name__)
        self.configure_logger(logging_level)

    def configure_logger(self, level=logger.INFO):
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_log_level,
                self.add_module_and_lineno,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                self.renderer,
                # structlog.processors.JSONRenderer(),
                # structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

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

    def add_module_and_lineno(
        self, logger: structlog.BoundLogger, name: str, event_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        # noinspection PyProtectedMember
        frame, module_str = structlog._frames._find_first_app_frame_and_name(
            additional_ignores=[__name__]
        )
        # frame has filename, caller and line number
        event_dict["module"] = module_str
        event_dict["lineno"] = frame.f_lineno
        return event_dict

    def renderer(
        self, logger: structlog.BoundLogger, name: str, event_dict: Dict[str, Any]
    ) -> str:
        event = event_dict["event"]
        module = "module: {0}".format(event_dict["module"])
        line_no = "line no: {0}".format(event_dict["lineno"])

        output = f"{module} | {line_no} | {event}"
        return output
