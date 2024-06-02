from typing import Any

from src.repositories.database.database_session_provider import DatabaseSessionProvider


class BaseSQLAlchemyRepository:
    def __init__(self, model_cls: Any, db_session_provider: DatabaseSessionProvider):
        self.model_cls = model_cls
        self.session = db_session_provider()

    def get_table_name(self):
        return self.model_cls.__table__.name

    def get_by_id(self, id: int):
        return self.session.query(self.model_cls).get(id)

    def get_all(self):
        return self.session.query(self.model_cls).all()

    def search(self, get_first=True, **filters):
        query = self.session.query(self.model_cls)

        for field, value in filters.items():
            if hasattr(self.model_cls, field):
                query = query.filter(getattr(self.model_cls, field) == value)

        if get_first:
            return query.first()
        else:
            return query.all()

    def create(self, entity):
        self.session.add(entity)
        self.session.commit()
        return entity

    def update(self, primary_key, update_data):
        entity = self.get_by_id(primary_key)
        if entity:
            for key, value in update_data.items():
                setattr(entity, key, value)
        self.session.commit()
        return entity

    def delete(
        self,
        entity,
    ):
        self.session.delete(entity)
        self.session.commit()
