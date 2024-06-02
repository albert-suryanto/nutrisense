from sqlalchemy import Column, Integer, String
from src.repositories.database.database_session_provider import Base


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
