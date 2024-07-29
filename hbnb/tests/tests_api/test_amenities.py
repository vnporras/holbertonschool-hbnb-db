import unittest
import uuid

from flask import Flask
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token
from src import create_app, db
from src.config import TestingConfig


def create_admin_user(app: Flask):
    with app.app_context():
        from src.models.user import User

        admin_user = User(
            email="owe@vic.ps",
            first_name="Owe",
            last_name="Vic",
            password="password",
            is_admin=True,
        )

        db.session.add(admin_user)
        db.session.commit()
        db.session.refresh(admin_user)

    return admin_user


class AmenityManagementTests(unittest.TestCase):

    def setUp(self):
        self.client = create_app(TestingConfig)
        self.app = self.client.test_client()
        self.app.testing = True

        self.admin_user = create_admin_user(self.client)

        with self.client.app_context():
            self.token = create_access_token(
                self.admin_user, additional_claims={"is_admin": True}
            )

            self.headers = {"Authorization": f"Bearer {self.token}"}

    def create_unique_amenity(self):
        unique_amenity_name = f"Test Amenity {uuid.uuid4()}"
        new_amenity = {"name": unique_amenity_name}
        response = self.app.post(
            "/amenities",
            json=new_amenity,
            headers=self.headers,
        )
        assert (
            response.status_code == 201
        ), f"Expected status code 201 but got {response.status_code}. Response: {response.json}"
        return response.get_json()["id"]

    def test_get_amenities(self):
        response = self.app.get("/amenities")
        self.assertEqual(
            response.status_code,
            200,
            f"Expected status code 200 but got {response.status_code}. Response: {response.json}",
        )
        self.assertIsInstance(
            response.get_json(),
            list,
            f"Expected response to be a list but got {type(response.get_json())}",
        )

    def test_post_amenity(self):
        unique_amenity_name = f"Test Amenity {uuid.uuid4()}"
        new_amenity = {"name": unique_amenity_name}
        response = self.app.post(
            "/amenities", json=new_amenity, headers=self.headers
        )
        self.assertEqual(
            response.status_code,
            201,
            f"Expected status code 201 but got {response.status_code}. Response: {response.json}",
        )
        amenity_data = response.get_json()
        self.assertEqual(
            amenity_data["name"],
            new_amenity["name"],
            f"Expected name to be {new_amenity['name']} but got {amenity_data['name']}",
        )
        self.assertIn("id", amenity_data, "Amenity ID not in response")
        self.assertIn("created_at", amenity_data, "Created_at not in response")
        self.assertIn("updated_at", amenity_data, "Updated_at not in response")

    def test_get_amenity(self):
        amenity_id = self.create_unique_amenity()
        response = self.app.get(f"/amenities/{amenity_id}")
        self.assertEqual(
            response.status_code,
            200,
            f"Expected status code 200 but got {response.status_code}. Response: {response.json}",
        )
        amenity_data = response.get_json()
        self.assertEqual(
            amenity_data["id"],
            amenity_id,
            f"Expected amenity ID to be {amenity_id} but got {amenity_data['id']}",
        )
        self.assertIn("name", amenity_data, "Name not in response")
        self.assertIn("created_at", amenity_data, "Created_at not in response")
        self.assertIn("updated_at", amenity_data, "Updated_at not in response")

    def test_put_amenity(self):
        amenity_id = self.create_unique_amenity()
        updated_amenity = {"name": f"Updated Amenity {uuid.uuid4()}"}
        response = self.app.put(
            f"/amenities/{amenity_id}",
            json=updated_amenity,
            headers=self.headers,
        )
        self.assertEqual(
            response.status_code,
            200,
            f"Expected status code 200 but got {response.status_code}. Response: {response.json}",
        )
        amenity_data = response.get_json()
        self.assertEqual(
            amenity_data["name"],
            updated_amenity["name"],
            f"Expected updated name to be {updated_amenity['name']} but got {amenity_data['name']}",
        )
        self.assertIn("id", amenity_data, "Amenity ID not in response")
        self.assertIn("created_at", amenity_data, "Created_at not in response")
        self.assertIn("updated_at", amenity_data, "Updated_at not in response")

    def test_delete_amenity(self):
        amenity_id = self.create_unique_amenity()
        response = self.app.delete(
            f"/amenities/{amenity_id}",
            headers=self.headers,
        )
        self.assertEqual(
            response.status_code,
            204,
            f"Expected status code 204 but got {response.status_code}. Response: {response.text}",
        )


if __name__ == "__main__":
    unittest.main()
