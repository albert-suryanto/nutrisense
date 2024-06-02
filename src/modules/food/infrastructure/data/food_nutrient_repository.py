from typing import List

from sqlalchemy import tuple_
from src.modules.food.domain.models.food_nutrient import FoodNutrient
from src.repositories.database.database_session_provider import (
    DatabaseSessionProvider,
    session_scope,
)
from src.system.logger import LoggerInterface


class FoodNutrientRepository:
    def __init__(
        self, logger: LoggerInterface, db_session_provider: DatabaseSessionProvider
    ):
        self.logger = logger
        self.db_session_provider = db_session_provider

    def get(self, food_id: int, nutrient_id: int):
        self.logger.info(
            f"Getting food nutrient with food_id: {food_id}, nutrient_id: {nutrient_id}"
        )

        with session_scope(self.db_session_provider) as session:
            food_nutrient = (
                session.query(FoodNutrient)
                .filter(FoodNutrient.food_id == food_id)
                .filter(FoodNutrient.nutrient_id == nutrient_id)
                .first()
            )
            if food_nutrient:
                session.expunge(food_nutrient)
        return food_nutrient

    def create(self, food_nutrient: FoodNutrient):
        self.logger.info(
            f"Creating food nutrient with food_id: {food_nutrient.food_id}, nutrient_id: {food_nutrient.nutrient_id}, amount: {food_nutrient.amount}, unit_name: {food_nutrient.unit_name}"
        )

        with session_scope(self.db_session_provider) as session:
            session.add(food_nutrient)
            session.commit()
            session.refresh(food_nutrient)
            session.expunge(food_nutrient)
            return food_nutrient

    def get_or_create(self, food_nutrient: FoodNutrient):
        self.logger.info(
            f"Getting or creating food nutrient with food_id: {food_nutrient.food_id}, nutrient_id: {food_nutrient.nutrient_id}, amount: {food_nutrient.amount}, unit_name: {food_nutrient.unit_name}"
        )

        result = self.get(food_nutrient.food_id, food_nutrient.nutrient_id)
        if not result:
            result = self.create(food_nutrient)
        return result

    def bulk_create(self, food_nutrients: List[FoodNutrient]):
        count = len(food_nutrients)
        self.logger.info(
            f"Receive {count} for bulk creating food nutrients with details"
        )

        with session_scope(self.db_session_provider) as session:
            existing_food_nutrients = (
                session.query(FoodNutrient)
                .filter(
                    tuple_(FoodNutrient.food_id, FoodNutrient.nutrient_id).in_(
                        [(item.food_id, item.nutrient_id) for item in food_nutrients]
                    )
                )
                .all()
            )

            existing_pairs = {
                (item.food_id, item.nutrient_id) for item in existing_food_nutrients
            }
            new_food_nutrients = [
                food_nutrient
                for food_nutrient in food_nutrients
                if (food_nutrient.food_id, food_nutrient.nutrient_id)
                not in existing_pairs
            ]

            new_count = len(new_food_nutrients)
            self.logger.info(
                f"Creating {new_count} new food nutrients and skipping {count - new_count} existing ones."
            )
            session.add_all(new_food_nutrients)
            session.commit()

        self.logger.info("Bulk creation of food nutrients completed.")
        return food_nutrients


# https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.add_all
# ### `session.add_all`

# - **ORM-Level Operation**: `session.add_all` is an ORM-level operation, meaning it uses the standard ORM facilities to add objects to the session. This method calls `session.add` for each object in the list.
# - **Individual Inserts**: Each object added via `session.add_all` is treated as an individual insert operation. SQLAlchemy generates individual SQL `INSERT` statements for each object.
# - **Full ORM Features**: This method ensures that all ORM features such as identity map, relationships, and other ORM-level mechanics are respected. This includes things like cascading, automatic expiration of objects, and attribute tracking.
# - **Session Management**: Objects added via `session.add_all` are fully managed by the session, meaning they participate in the unit of work and are subject to all session-level operations.

# ### `session.bulk_save_objects`

# - **Core-Level Operation**: `session.bulk_save_objects` is a Core-level operation, meaning it bypasses some ORM features for the sake of performance. It directly uses SQLAlchemy Core to perform the inserts.
# - **Batch Inserts**: This method aims to perform batch inserts, potentially reducing the number of SQL `INSERT` statements by grouping them into larger, more efficient batches.
# - **Limited ORM Features**: It does not track changes to the objects after they are inserted, does not handle relationships, and does not put the objects into the session. This method is more suitable for bulk loading scenarios where the overhead of full ORM features is not needed.
# - **Performance**: `session.bulk_save_objects` can be significantly faster than `session.add_all` for large numbers of inserts because it minimizes the overhead of ORM mechanics.

# ### When to Use Which

# - **`add_all`**: Use `add_all` when you need full ORM functionality, such as when dealing with complex object relationships, cascading, and other ORM features. It's appropriate for scenarios where you want the session to fully manage the lifecycle of objects.
# - **`bulk_save_objects`**: Use `bulk_save_objects` for performance-critical bulk insert operations where you don't need the overhead of full ORM features. This is ideal for initial data loading or batch processing tasks where the objects don't need to be fully tracked by the session.

# ### Foreign Key Constraints with `bulk_save_objects`

# No, `bulk_save_objects` does not check for existing foreign keys or enforce any ORM-level validations. It bypasses many of the ORM features to improve performance, including foreign key checks, relationship management, and other validations that SQLAlchemy ORM typically handles.

# To ensure foreign key constraints are respected while using `bulk_save_objects`, you should manually check that the foreign keys (e.g., `food_id` and `nutrient_id`) exist in their respective tables before performing the bulk save operation.
