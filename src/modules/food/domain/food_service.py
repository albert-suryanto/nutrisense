from datetime import datetime
from tqdm import tqdm
from src.modules.food.domain.models.category import Category
from src.modules.food.domain.models.food import Food
from src.modules.food.domain.models.food_nutrient import FoodNutrient
from src.modules.food.domain.models.nutrient import Nutrient
from src.modules.llm.domain.embedding_service import EmbeddingService
from src.modules.food.infrastructure.data.category_repository import CategoryRepository
from src.modules.food.infrastructure.data.food_nutrient_repository import (
    FoodNutrientRepository,
)
from src.modules.food.infrastructure.data.food_repository import FoodRepository
from src.modules.food.infrastructure.data.nutrient_repository import NutrientRepository
from src.system.logger import LoggerInterface


class FoodService:
    def __init__(
        self,
        logger: LoggerInterface,
        category_repo: CategoryRepository,
        nutrient_repo: NutrientRepository,
        food_repo: FoodRepository,
        food_nutrient_repo: FoodNutrientRepository,
        embedding_service: EmbeddingService,
    ):
        self.logger = logger
        self.embedding_service = embedding_service
        self.category_repo = category_repo
        self.nutrient_repo = nutrient_repo
        self.food_repo = food_repo
        self.food_nutrient_repo = food_nutrient_repo

    def load_data(self, data):
        count = len(data)
        for index, item in enumerate(tqdm(data)):
            self.logger.info(
                f"Processing item {index+1}/{count}: {item['description']}"
            )
            foods_vector = self.embedding_service.generate_embedding(
                item['description']
            )

            category = Category(name=item['foodCategory']['description'])
            category = self.category_repo.get_or_create(category)

            publication_date = datetime.strptime(
                item['publicationDate'], "%m/%d/%Y"
            ).date()
            food = Food(
                name=item['description'],
                category_id=category.id,
                publication_date=publication_date,
                foods_vector=foods_vector,
            )
            food = self.food_repo.get_or_create(food)

            nutrients_to_process = [
                Nutrient(name=nutrient_data['name'])
                for nutrient_data in item['foodNutrients']
            ]
            nutrients = self.nutrient_repo.bulk_get_or_create(nutrients_to_process)
            food_nutrients = []
            for nutrient_data in item['foodNutrients']:
                nutrient = next(
                    (item for item in nutrients if item.name == nutrient_data['name']),
                    None,
                )
                if nutrient is None:
                    self.logger.error(
                        f"Nutrient {nutrient_data['name']} not found in database"
                    )
                    raise Exception(
                        f"Nutrient {nutrient_data['name']} not found in database for food {food.name}"
                    )

                amount = (
                    nutrient_data['amount']
                    if nutrient_data['amount'] is not None
                    else 0
                )

                food_nutrient = FoodNutrient(
                    food_id=food.id,
                    nutrient_id=nutrient.id,
                    amount=amount,
                    unit_name=nutrient_data['unitName'],
                )
                food_nutrients.append(food_nutrient)

            self.food_nutrient_repo.bulk_create(food_nutrients)
