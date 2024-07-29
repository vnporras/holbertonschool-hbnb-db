import unittest
import uuid

from flask_jwt_extended import create_access_token

from src import create_app, db
from src.models.user import User
from src.config import TestingConfig
from src.models.city import City


class PlaceManagementTests(unittest.TestCase):

    def setUp(self):
        self.client = create_app(TestingConfig)
        self.app = self.client.test_client()

        self.city = self.create_unique_city()
        self.admin_user = self.create_admin_user()

        with self.client.app_context():
            self.token = create_access_token(self.admin_user)
            self.headers = {"Authorization": f"Bearer {self.token}"}

    def create_unique_city(self):
        new_city = City(name=f"Test City {uuid.uuid4()}", country_code="UY")

        with self.client.app_context():
            db.session.add(new_city)
            db.session.commit()
            db.session.refresh(new_city)

        return new_city

    def create_admin_user(self):
        admin_user = User(
            email="mo@lojo.ar",
            first_name="Mo",
            last_name="Lojo",
            password="password",
            is_admin=True,
        )

        with self.client.app_context():
            db.session.add(admin_user)
            db.session.commit()
            db.session.refresh(admin_user)

        return admin_user

    def test_get_places(self):
        response = self.app.get("/places")
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

    def test_post_place(self):
        new_place = {
            "name": "Cozy Cottage",
            "description": "A cozy cottage in the countryside.",
            "address": "123 Country Lane",
            "latitude": 34.052235,
            "longitude": -118.243683,
            "host_id": self.admin_user.id,
            "city_id": self.city.id,
            "price_per_night": 100,
            "number_of_rooms": 2,
            "number_of_bathrooms": 1,
            "max_guests": 4,
        }
        response = self.app.post(
            "/places", json=new_place, headers=self.headers
        )
        self.assertEqual(
            response.status_code,
            201,
            f"Expected status code 201 but got {response.status_code}. Response: {response.json}",
        )
        place_data = response.get_json()
        for key in new_place:
            self.assertEqual(
                place_data[key],
                new_place[key],
                f"Expected {key} to be {new_place[key]} but got {place_data[key]}",
            )
        self.assertIn("id", place_data, "Place ID not in response")
        self.assertIn("created_at", place_data, "Created_at not in response")
        self.assertIn("updated_at", place_data, "Updated_at not in response")
        self.place_id = place_data["id"]  # Store place ID for further tests

    def test_get_place(self):
        self.test_post_place()  # Ensure a place is created
        response = self.app.get(f"/places/{self.place_id}")
        self.assertEqual(
            response.status_code,
            200,
            f"Expected status code 200 but got {response.status_code}. Response: {response.json}",
        )
        place_data = response.get_json()
        new_place = {
            "name": "Cozy Cottage",
            "description": "A cozy cottage in the countryside.",
            "address": "123 Country Lane",
            "latitude": 34.052235,
            "longitude": -118.243683,
            "host_id": place_data["host_id"],
            "city_id": place_data["city_id"],
            "price_per_night": 100,
            "number_of_rooms": 2,
            "number_of_bathrooms": 1,
            "max_guests": 4,
        }
        for key in new_place:
            self.assertEqual(
                place_data[key],
                new_place[key],
                f"Expected {key} to be {new_place[key]} but got {place_data[key]}",
            )
        self.assertIn("id", place_data, "Place ID not in response")
        self.assertIn("created_at", place_data, "Created_at not in response")
        self.assertIn("updated_at", place_data, "Updated_at not in response")

    def test_put_place(self):
        self.test_post_place()  # Ensure a place is created
        updated_place = {
            "name": "Lakeside Cabin",
            "description": "A charming cabin by the lake.",
            "address": "101 Lakeside Drive",
            "latitude": 38.89511,
            "longitude": -77.03637,
            "host_id": self.admin_user.id,
            "city_id": self.city.id,
            "price_per_night": 180,
            "number_of_rooms": 3,
            "number_of_bathrooms": 2,
            "max_guests": 6,
        }
        response = self.app.put(
            f"/places/{self.place_id}",
            json=updated_place,
            headers=self.headers,
        )
        self.assertEqual(
            response.status_code,
            200,
            f"Expected status code 200 but got {response.status_code}. Response: {response.json}",
        )
        place_data = response.get_json()
        for key in updated_place:
            self.assertEqual(
                place_data[key],
                updated_place[key],
                f"Expected updated {key} to be {updated_place[key]} but got {place_data[key]}",
            )
        self.assertIn("id", place_data, "Place ID not in response")
        self.assertIn("created_at", place_data, "Created_at not in response")
        self.assertIn("updated_at", place_data, "Updated_at not in response")

    def test_delete_place(self):
        self.test_post_place()  # Ensure a place is created
        response = self.app.delete(
            f"/places/{self.place_id}", headers=self.headers
        )
        self.assertEqual(
            response.status_code,
            204,
            f"Expected status code 204 but got {response.status_code}. Response: {response.text}",
        )


if __name__ == "__main__":
    unittest.main()
