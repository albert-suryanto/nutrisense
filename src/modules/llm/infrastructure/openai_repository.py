import openai
from src.system.logger import LoggerInterface


class OpenAIRepository:
    def __init__(self, logger: LoggerInterface, api_key: str, embedding_model: str):
        self.logger = logger
        openai.api_key = api_key
        self.embedding_model = embedding_model

    def generate_embedding(self, text: str):
        self.logger.info(f"Generating embedding for text: {text}")

        text = text.replace("\n", " ")
        response = openai.embeddings.create(input=[text], model=self.embedding_model)
        embedding = response.data[0].embedding
        return embedding
