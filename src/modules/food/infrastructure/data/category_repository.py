from src.modules.food.domain.models.category import Category
from src.repositories.database.database_session_provider import (
    DatabaseSessionProvider,
    session_scope,
)
from src.system.logger import LoggerInterface


class CategoryRepository:
    def __init__(
        self, logger: LoggerInterface, db_session_provider: DatabaseSessionProvider
    ):
        self.logger = logger
        self.db_session_provider = db_session_provider

    def get(self, name: str):
        self.logger.info(f"Getting category with name: {name}")
        with session_scope(self.db_session_provider) as session:
            category = session.query(Category).filter(Category.name == name).first()
        return category

    def create(self, category: Category):
        self.logger.info(f"Creating category with name: {category.name}")
        with session_scope(self.db_session_provider) as session:
            session.add(category)
            session.commit()
        return category

    def get_or_create(self, category: Category):
        self.logger.info(f"Getting or creating category with name: {category.name}")
        result = self.get(category.name)
        if not result:
            result = self.create(category)
        return result
