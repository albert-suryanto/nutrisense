from dependency_injector import containers, providers
from src.modules.llm.domain.embedding_service import EmbeddingService
from src.repositories.database.database_session_provider import DatabaseSessionProvider
from src.modules.food.domain.food_service import FoodService
from src.modules.food.infrastructure.data.category_repository import CategoryRepository
from src.modules.food.infrastructure.data.food_repository import FoodRepository
from src.modules.food.infrastructure.data.food_nutrient_repository import (
    FoodNutrientRepository,
)
from src.modules.food.infrastructure.data.nutrient_repository import NutrientRepository
from src.system.logger import LoggerInterface


class FoodContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    logger: LoggerInterface = providers.Dependency()
    embedding_service: EmbeddingService = providers.Dependency()
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.modules.food",
        ]
    )

    db_session_provider = providers.Factory(
        DatabaseSessionProvider, db_uri=config.databases.main.url
    )
    category_repo = providers.Singleton(
        CategoryRepository, logger=logger, db_session_provider=db_session_provider
    )
    food_nutrient_repo = providers.Singleton(
        FoodNutrientRepository, logger=logger, db_session_provider=db_session_provider
    )
    food_repo = providers.Singleton(
        FoodRepository, logger=logger, db_session_provider=db_session_provider
    )
    nutrient_repo = providers.Singleton(
        NutrientRepository, logger=logger, db_session_provider=db_session_provider
    )

    food_service = providers.Factory(
        FoodService,
        logger=logger,
        category_repo=category_repo,
        nutrient_repo=nutrient_repo,
        food_repo=food_repo,
        food_nutrient_repo=food_nutrient_repo,
        embedding_service=embedding_service,
    )
