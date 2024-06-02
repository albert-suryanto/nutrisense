from dependency_injector import containers, providers
from src.system.strcutlog_logger import StructLogLogger
from src.modules.llm.llm_modules import LLMContainer
from src.modules.food.food_modules import FoodContainer


class Containers(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.utils.helpers",
        ]
    )

    # Options: [LoggingLogger, StructLogLogger]
    logger = providers.Singleton(StructLogLogger)


class Application(containers.DeclarativeContainer):
    config = providers.Configuration()

    container = Containers()
    llm_package = providers.Container(
        LLMContainer,
        config=config,
        logger=container.logger,
    )
    food_package = providers.Container(
        FoodContainer,
        config=config,
        logger=container.logger,
        embedding_service=llm_package.embedding_service,
    )
