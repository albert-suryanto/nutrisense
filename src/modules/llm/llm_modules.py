from dependency_injector import containers, providers
from src.modules.llm.domain.embedding_service import EmbeddingService
from src.modules.llm.infrastructure.openai_repository import OpenAIRepository
from src.system.logger import LoggerInterface


class LLMContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    logger: LoggerInterface = providers.Dependency()

    wiring_config = containers.WiringConfiguration(modules=["src.modules.llm"])

    openai_repo = providers.Singleton(
        OpenAIRepository,
        logger=logger,
        api_key=config.llms.openai.api_key,
        embedding_model=config.llms.openai.embedding_model,
    )
    embedding_service = providers.Singleton(
        EmbeddingService, logger=logger, llm_repo=openai_repo
    )
