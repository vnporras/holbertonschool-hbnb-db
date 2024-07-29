"""
This module exports a Repository that persists data in a pickle file
"""

import pickle
from typing import Optional
from src.persistence.repository import Repository
from utils.constants import PICKLE_STORAGE_FILENAME


class PickleRepository(Repository):
    """Pickle Repository"""

    __filename = PICKLE_STORAGE_FILENAME

    def __init__(self, filename: Optional[str] = None, *args, **kw) -> None:
        """Calls reload method"""

        super().__init__(*args, **kw)

        if filename:
            self.__filename = filename

        self.reload()

    def _save_to_file(self):
        """Helper method to save the current object data to the file"""
        with open(self.__filename, "wb") as file:
            pickle.dump(self._data, file)

    def get_all(self, model_name: str) -> list:
        """Get all objects of a given model"""
        return self._data[model_name]

    def get(self, model_name: str, obj_id: str):
        """Get an object by its ID"""
        for obj in self._data[model_name]:
            if obj.id == obj_id:
                return obj
        return None

    def reload(self):
        """Reloads the data from the pickle file"""
        try:
            with open(self.__filename, "rb") as file:
                self._data = pickle.load(file)
        except FileNotFoundError:
            self._save_to_file()

    def save(self, obj, save_to_file=True):
        """Save an object"""
        self._data[obj.__class__.__name__].append(obj)
        if save_to_file:
            self._save_to_file()

    def update(self, obj):
        """Update an object"""
        for i, o in enumerate(self._data[obj.__class__.__name__]):
            if o.id == obj.id:
                self._data[obj.__class__.__name__][i] = obj
                self._save_to_file()
                return obj

    def delete(self, obj) -> bool:
        """Delete an object"""
        for i, o in enumerate(self._data[obj.__class__.__name__]):
            if o.id == obj.id:
                del self._data[obj.__class__.__name__][i]
                break

        self._save_to_file()
        return True
