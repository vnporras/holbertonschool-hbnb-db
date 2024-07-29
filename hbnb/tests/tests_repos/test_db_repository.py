from src.config import TestingConfig
from src import db, create_app
from src.persistence.db import DBRepository
import unittest

import sqlalchemy.orm as so
import sqlalchemy as sa


class DummyModel(db.Model):
    id: so.Mapped[int] = sa.Column(
        sa.Integer, primary_key=True, autoincrement=True
    )


class TestDBRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.app = create_app(TestingConfig)

        cls.models = {"DummyModel": DummyModel}
        cls.data = {}

        with cls.app.app_context():
            cls.repo = DBRepository(cls.models, cls.data)

    def test_get_all(self):
        with self.app.app_context():
            result = self.repo.get_all("DummyModel")
        self.assertIsInstance(
            result, list, f"Expected a list but got {type(result)}"
        )

    def test_get(self):
        with self.app.app_context():
            result = self.repo.get("DummyModel", 1)
        self.assertIsNone(result, "Expected None")

    def test_reload(self):
        with self.app.app_context():
            self.repo.reload()

    def test_save(self):
        obj = DummyModel()

        with self.app.app_context():
            self.repo.save(obj)

            dummy = self.repo.get("DummyModel", obj.id)

        self.assertIsNotNone(dummy, "Expected not None")

    def test_update(self):
        with self.app.app_context():
            result = self.repo.update("DummyModel")

        self.assertIsNotNone(result, "Expected None")

    def test_delete(self):
        with self.app.app_context():
            obj = DummyModel()
            db.session.add(obj)
            db.session.commit()

            result = self.repo.delete(obj)

        self.assertTrue(result, "Expected True")


if __name__ == "__main__":
    unittest.main()
