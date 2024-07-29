""" This module is responsible for selecting the repository
to be used based on the environment variable REPOSITORY_ENV_VAR."""

from utils.constants import Repos


def get_repo(name: str):
    """Get the repository based on the name"""
    if name == Repos.MEMORY.value:
        from src.persistence.memory import MemoryRepository

        return MemoryRepository
    elif name == Repos.DB.value:
        from src.persistence.db import DBRepository

        return DBRepository
    elif name == Repos.PICKLE.value:
        from src.persistence.pickled import PickleRepository

        return PickleRepository
    else:
        from src.persistence.file import FileRepository

        return FileRepository
