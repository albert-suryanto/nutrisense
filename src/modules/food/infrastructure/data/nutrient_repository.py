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

    def bulk_get_or_create(self, nutrients: List[Nutrient]):
        count = len(nutrients)
        self.logger.info(
            f"Bulk get or create {count} nutrients with names: {[nutrient.name for nutrient in nutrients]}"
        )

        with session_scope(self.db_session_provider) as session:
            existing_nutrients = (
                session.query(Nutrient)
                .filter(Nutrient.name.in_([item.name for item in nutrients]))
                .all()
            )

            existing_nutrient_dict = {
                nutrient.name: nutrient for nutrient in existing_nutrients
            }
            new_nutrients = [
                nutrient
                for nutrient in nutrients
                if nutrient.name not in existing_nutrient_dict
            ]

            if new_nutrients:
                new_count = len(new_nutrients)
                self.logger.info(
                    f"Creating {new_count} new nutrients and skipping {count - new_count} existing ones."
                )

                session.add_all(new_nutrients)
                session.commit()

                existing_nutrient_dict.update(
                    {nutrient.name: nutrient for nutrient in new_nutrients}
                )

            result_list = list(existing_nutrient_dict.values())
            for nutrient in result_list:
                session.refresh(nutrient)
                session.expunge(nutrient)

        self.logger.info(
            f"Created {len(new_nutrients)} new nutrients and found {len(existing_nutrients)} existing nutrients."
        )

        return result_list
