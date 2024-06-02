from sqlalchemy import Column, Integer, String
from src.repositories.database.database_session_provider import Base


class Nutrient(Base):
    __tablename__ = 'nutrients'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
