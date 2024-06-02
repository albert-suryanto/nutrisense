from src.modules.llm.infrastructure.openai_repository import OpenAIRepository
from src.system.logger import LoggerInterface


class EmbeddingService:
    def __init__(self, logger: LoggerInterface, llm_repo: OpenAIRepository):
        self.logger = logger
        self.llm_repo = llm_repo

    def generate_embedding(self, text: str):
        return self.llm_repo.generate_embedding(text)
