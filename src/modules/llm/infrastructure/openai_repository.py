import httpx
import openai
from src.system.logger import LoggerInterface
from tenacity import (
    RetryCallState,
    Retrying,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)


class OpenAIRepository:
    def __init__(self, logger: LoggerInterface, api_key: str, embedding_model: str):
        self.logger = logger
        openai.api_key = api_key
        self.embedding_model = embedding_model

    def _log_attempt_number(self, retry_state: RetryCallState):
        self.logger.warning(f"Attempt number: {retry_state.attempt_number}")

    def generate_embedding(self, text: str):
        self.logger.info(f"Generating embedding for text: {text}")
        retrying = Retrying(
            stop=stop_after_attempt(5),
            wait=wait_exponential(multiplier=1, min=4, max=10),
            retry=retry_if_exception_type((openai.OpenAIError, httpx.ConnectError)),
            after=self._log_attempt_number,
        )

        text = text.replace("\n", " ")

        try:
            for attempt in retrying:
                with attempt:
                    response = openai.embeddings.create(
                        input=[text], model=self.embedding_model
                    )
                    embedding = response.data[0].embedding
                    return embedding
        except Exception as e:
            self.logger.error(f"Failed to generate embedding: {e}")
            raise
