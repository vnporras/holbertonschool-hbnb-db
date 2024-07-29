"""
DB Repository
"""

from src import db
from src.models.base import Base
from src.persistence.repository import Repository

from sqlalchemy.orm import Query


class DBRepository(Repository):
    """Dummy DB repository"""

    def get_all(self, model_name: str) -> list:
        """Returns all objects of a given model"""
        result: Query = db.session.query(self.models[model_name])

        return result.all()

    def get(self, model_name: str, obj_id: str) -> Base | None:
        """Returns an object by its ID"""
        result = db.session.get(self.models[model_name], obj_id)

        return result

    def reload(self) -> None:
        """Not needed"""

    def save(self, obj: Base) -> None:
        """Save an object to the repository"""
        db.session.add(obj)
        db.session.commit()

    def update(self, obj: Base) -> Base | None:
        """Update an object in the repository"""
        db.session.commit()

        return obj

    def delete(self, obj: Base) -> bool:
        """Delete an object from the repository"""
        db.session.delete(obj)
        db.session.commit()

        return True
