from dependency_injector.wiring import Provide, inject
from datetime import datetime
from src.system.logger import LoggerInterface
from src.container import Containers


@inject
def validate_date_string_format(
    date_str: str,
    format: str = "%Y-%m-%d",
    logger: LoggerInterface = Provide[Containers.logger],
) -> bool:
    try:
        datetime.strptime(date_str, format)
        return True
    except ValueError as e:
        logger.error(e)
        return False
