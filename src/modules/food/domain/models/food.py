from sqlalchemy import Column, Float, Integer, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from src.repositories.database.database_session_provider import Base


class Food(Base):
    __tablename__ = 'foods'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    publication_date = Column(Date)
    foods_vector = Column(ARRAY(Float))

    category = relationship("Category")
    nutrients = relationship("FoodNutrient", back_populates="food")
