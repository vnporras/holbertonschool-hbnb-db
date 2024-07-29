""" Repository pattern for data access layer """

from abc import ABC, abstractmethod
from typing import Any
from flask import Flask

from src.persistence import get_repo


class Repository(ABC):
    """Abstract class for repository pattern"""

    def __init__(self, models: dict, data: dict) -> None:
        """Base constructor for the repository"""
        self.models: dict[str, Any] = models
        self._data: dict[str, list] = data

    @abstractmethod
    def reload(self) -> None:
        """Reload data to the repository"""

    @abstractmethod
    def get_all(self, model_name: str) -> list:
        """Get all objects of a model"""

    @abstractmethod
    def get(self, model_name: str, id: str) -> Any | None:
        """Get an object by id"""

    @abstractmethod
    def save(self, obj) -> None:
        """Save an object"""

    @abstractmethod
    def update(self, obj) -> Any:
        """Update an object"""

    @abstractmethod
    def delete(self, obj) -> bool:
        """Delete an object"""


class RepositoryManager:
    """Manages the initialization of the repository in the Flask App"""

    models: dict = {}
    _data: dict = {}

    def init_app(self, app: Flask, models: list | None = None) -> None:
        """Initialize the repository with the app and models"""
        self.app = app

        if models:
            for model in models:
                self.__register_model(model)

        Repo = get_repo(app.config["REPOSITORY"])

        self.repo = Repo(self.models, self._data)

    def __register_model(self, *models) -> None:
        """Register models in the repository"""
        for model in models:
            self.models[model.__name__] = model
            self._data[model.__name__] = []

    def get(self, model_name: str, obj_id: str) -> Any | None:
        """Get an object by id"""
        return self.repo.get(model_name, obj_id)

    def get_all(self, model_name: str) -> list:
        """Get all objects of a model"""
        return self.repo.get_all(model_name)

    def save(self, obj) -> None:
        """Save an object"""
        return self.repo.save(obj)

    def update(self, obj) -> None:
        """Update an object"""
        return self.repo.update(obj)

    def delete(self, obj) -> bool:
        """Delete an object"""
        return self.repo.delete(obj)
