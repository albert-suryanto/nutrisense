from sqlalchemy import text
from src.modules.food.domain.models.food import Food
from src.repositories.database.database_session_provider import (
    DatabaseSessionProvider,
    session_scope,
)
from src.system.logger import LoggerInterface


class FoodRepository:
    def __init__(
        self, logger: LoggerInterface, db_session_provider: DatabaseSessionProvider
    ):
        self.logger = logger
        self.db_session_provider = db_session_provider

    def get(self, name: str):
        self.logger.info(f"Getting food with name: {name}")
        with session_scope(self.db_session_provider) as session:
            food = session.query(Food).filter(Food.name == name).first()
            if food:
                session.expunge(food)
        return food

    def create(self, food: Food):
        self.logger.info(
            f"Creating food with name: {food.name}, category_id: {food.category_id}, publication_date: {food.publication_date}, foods_vector: {food.foods_vector}"
        )
        with session_scope(self.db_session_provider) as session:
            session.add(food)
            session.commit()
            session.refresh(food)
            session.expunge(food)
            return food

    def get_or_create(self, food: Food):
        self.logger.info(
            f"Getting or creating food with name: {food.name}, category_id: {food.category_id}, publication_date: {food.publication_date}, foods_vector: {food.foods_vector}"
        )

        result = self.get(food.name)
        if result is None:
            result = self.create(food)
        return result

    def get_food_by_food_vector(self, foods_vector, top_k=5):
        self.logger.info(f"Getting food by food vector with top_k: {top_k}")

        with session_scope(self.db_session_provider) as session:
            query = text(
                """
                SELECT id, food_name, category_id, publication_date,
                    foods_vector <=> :foods_vector AS distance
                FROM foods
                ORDER BY distance
                LIMIT :top_k
                """
            )
            result = session.execute(
                query, {"foods_vector": foods_vector, "top_k": top_k}
            ).fetchmany()
            return result
