from typing import Optional
from uuid import uuid4
from src.persistence.pickled import PickleRepository
import unittest


class DummyModel:
    id: str
    name: str = ""

    def __init__(self, name: str, id: Optional[str] = None) -> None:
        self.id = id or str(uuid4())
        self.name = name

    def to_dict(self):
        return {"id": self.id, "name": self.name}


class TestPickleRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.models = {"DummyModel": DummyModel}
        cls.data = {"DummyModel": []}

        cls.repo = PickleRepository("test_file.pkl", cls.models, cls.data)

    def test_get_all(self):
        result = self.repo.get_all("DummyModel")
        self.assertIsInstance(
            result, list, f"Expected a list but got {type(result)}"
        )

        self.repo._data["DummyModel"] = [
            DummyModel("dummy"),
            DummyModel("dummy2"),
        ]

        results = self.repo.get_all("DummyModel")

        self.assertEqual(len(results), 2, "Expected 2")

    def test_get(self):
        result = self.repo.get("DummyModel", 1)

        self.assertIsNone(result, "Expected None")

        obj = DummyModel("dummy")

        self.repo._data["DummyModel"] = [obj]

        result = self.repo.get("DummyModel", obj.id)

        self.assertIsNotNone(result, "Expected not None")

    def test_reload(self):
        self.repo.reload()

    def test_save(self):
        obj = DummyModel("duuumy")

        self.repo.save(obj)

        dummy = self.repo.get("DummyModel", obj.id)

        self.assertIsNotNone(dummy, "Expected not None")
        self.assertEqual(dummy.name, "duuumy", "Expected 'duuumy'")

    def test_update(self):
        obj = DummyModel("dummy")

        self.repo._data["DummyModel"] = [obj]

        obj.name = "updated"

        result = self.repo.update(obj)

        self.assertIsNotNone(result, "Expected None")

        self.assertEqual(result.name, "updated", "Expected 'updated'")

    def test_delete(self):
        obj = DummyModel("delete me")

        self.repo._data["DummyModel"] = [obj]

        result = self.repo.delete(obj)

        self.assertTrue(result, "Expected True")
