from typing import List
from src.modules.food.domain.models.nutrient import Nutrient
from src.repositories.database.database_session_provider import (
    DatabaseSessionProvider,
    session_scope,
)
from src.system.logger import LoggerInterface


class NutrientRepository:
    def __init__(
        self, logger: LoggerInterface, db_session_provider: DatabaseSessionProvider
    ):
        self.logger = logger
        self.db_session_provider = db_session_provider

    def get(self, name: str):
        self.logger.info(f"Getting nutrient with name: {name}")
        with session_scope(self.db_session_provider) as session:
            nutrient = session.query(Nutrient).filter(Nutrient.name == name).first()
            if nutrient:
                session.expunge(nutrient)
        return nutrient

    def create(self, nutrient: Nutrient):
        self.logger.info(f"Creating nutrient with name: {nutrient.name}")
        with session_scope(self.db_session_provider) as session:
            session.add(nutrient)
            session.commit()
            session.refresh(nutrient)
            session.expunge(nutrient)
            return nutrient

    def get_or_create(self, nutrient: Nutrient):
        self.logger.info(f"Getting or creating nutrient with name: {nutrient.name}")

        result = self.get(nutrient.name)
        if not result:
            result = self.create(nutrient)
        return result

    def bulk_create(self, nutrients: List[Nutrient]):
        count = len(nutrients)
        self.logger.info(f"Receive {count} for bulk creating nutrients with details")

        with session_scope(self.db_session_provider) as session:
            existing_nutrient_ids = (
                session.query(Nutrient.id)
                .filter(Nutrient.id.in_([item.id for item in nutrients]))
                .all()
            )

            existing_ids = {id_tuple[0] for id_tuple in existing_nutrient_ids}

            new_nutrients = [
                nutrient for nutrient in nutrients if nutrient.id not in existing_ids
            ]

            new_count = len(new_nutrients)
            self.logger.info(
                f"Creating {new_count} new nutrients and skipping {count - new_count} existing ones."
            )

            session.add_all(new_nutrients)
            session.commit()
            session.refresh(new_nutrients)
            session.expunge(new_nutrients)

        self.logger.info("Bulk creation of food nutrients completed.")
        return new_nutrients
