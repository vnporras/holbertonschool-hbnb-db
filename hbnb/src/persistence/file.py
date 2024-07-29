"""
This module exports a Repository that persists data in a JSON file
"""

from datetime import datetime
import json
from typing import Optional

from flask import current_app
from src.models.base import Base
from src.persistence.repository import Repository
from utils.constants import FILE_STORAGE_FILENAME


class FileRepository(Repository):
    """File Repository"""

    __filename = FILE_STORAGE_FILENAME

    def __init__(self, filename: Optional[str] = None, *args, **kw) -> None:
        """Calls reload method"""
        super().__init__(*args, **kw)

        if filename:
            self.__filename = filename

        self.reload()

    def _save_to_file(self):
        """Helper method to save the current object data to the file"""
        serialized = {
            k: [v.to_dict() for v in l if type(v) is not dict]
            for k, l in self._data.items()
        }

        with open(self.__filename, "w") as file:
            json.dump(serialized, file)

    def get_all(self, model_name: str):
        """Get all objects of a given model"""
        return self._data.get(model_name, [])

    def get(self, model_name: str, obj_id: str):
        """Get an object by its ID"""
        for obj in self.get_all(model_name):
            if obj.id == obj_id:
                return obj
        return None

    def reload(self):
        """Reloads the data from the file"""
        file_data = {}
        try:
            with open(self.__filename, "r") as file:
                file_data = json.load(file)
        except FileNotFoundError:
            self._save_to_file()

        for model, data in file_data.items():
            for item in data:
                instance: Base = self.models[model](**item)

                if "created_at" in item:
                    instance.created_at = datetime.fromisoformat(
                        item["created_at"],
                    )
                if "updated_at" in item:
                    instance.updated_at = datetime.fromisoformat(
                        item["updated_at"],
                    )

                self.save(data=instance, save_to_file=False)

    def save(self, data: Base, save_to_file=True):
        """Save an object to the repository"""
        model: str = data.__class__.__name__

        if model not in self._data:
            self._data[model] = []

        self._data[model].append(data)

        if save_to_file:
            self._save_to_file()

    def update(self, obj: Base):
        """Update an object in the repository"""
        cls = obj.__class__.__name__

        for i, o in enumerate(self._data[cls]):
            if o.id == obj.id:
                obj.updated_at = datetime.now()
                self._data[cls][i] = obj
                self._save_to_file()
                return obj

        return None

    def delete(self, obj: Base):
        """Delete an object from the repository"""
        class_name = obj.__class__.__name__

        if obj not in self._data[class_name]:
            return False

        self._data[class_name].remove(obj)

        self._save_to_file()

        return True
