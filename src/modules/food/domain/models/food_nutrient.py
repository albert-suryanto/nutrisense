from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from src.repositories.database.database_session_provider import Base


class FoodNutrient(Base):
    __tablename__ = 'food_nutrients'

    food_id = Column(Integer, ForeignKey('foods.id'), primary_key=True, nullable=False)
    nutrient_id = Column(
        Integer, ForeignKey('nutrients.id'), primary_key=True, nullable=False
    )
    unit_name = Column(String, primary_key=True, nullable=False)
    amount = Column(Float, nullable=False)

    food = relationship("Food", back_populates="nutrients")
    nutrient = relationship("Nutrient")
