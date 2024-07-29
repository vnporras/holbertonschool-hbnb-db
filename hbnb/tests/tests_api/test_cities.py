import unittest
import uuid

from flask_jwt_extended import create_access_token

from src import create_app, db
from src.config import TestingConfig
from src.models.city import City
from src.models.user import User


class CityManagementTests(unittest.TestCase):

    def setUp(self):
        self.client = create_app(TestingConfig)
        self.app = self.client.test_client()
        self.app.testing = True

        self.admin_user = self.create_admin_user()

        with self.client.app_context():
            self.token = create_access_token(
                self.admin_user, additional_claims={"is_admin": True}
            )
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
            email="jokhul@hil.sr",
            first_name="Jokhul",
            last_name="Hil",
            password="password",
            is_admin=True,
        )

        with self.client.app_context():
            db.session.add(admin_user)
            db.session.commit()
            db.session.refresh(admin_user)

        return admin_user

    def test_get_cities(self):
        response = self.app.get("/cities")
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

    def test_post_city(self):
        new_city = {"name": f"Test City {uuid.uuid4()}", "country_code": "UY"}
        response = self.app.post(
            "/cities", json=new_city, headers=self.headers
        )
        self.assertEqual(
            response.status_code,
            201,
            f"Expected status code 201 but got {response.status_code}. Response: {response.json}",
        )
        city_data = response.get_json()
        self.assertEqual(
            city_data["name"],
            new_city["name"],
            f"Expected city name to be {new_city['name']} but got {city_data['name']}",
        )
        self.assertEqual(
            city_data["country_code"],
            new_city["country_code"],
            f"Expected country code to be {new_city['country_code']} but got {city_data['country_code']}",
        )
        self.assertIn("id", city_data, "City ID not in response")
        self.assertIn("created_at", city_data, "Created_at not in response")
        self.assertIn("updated_at", city_data, "Updated_at not in response")

    def test_get_city(self):
        city = self.create_unique_city()
        response = self.app.get(f"/cities/{city.id}")
        self.assertEqual(
            response.status_code,
            200,
            f"Expected status code 200 but got {response.status_code}. Response: {response.json}",
        )
        city_data = response.get_json()
        self.assertEqual(
            city_data["id"],
            city.id,
            f"Expected city ID to be {city.id} but got {city_data['id']}",
        )
        self.assertIn("name", city_data, "Name not in response")
        self.assertIn(
            "country_code", city_data, "Country code not in response"
        )
        self.assertIn("created_at", city_data, "Created_at not in response")
        self.assertIn("updated_at", city_data, "Updated_at not in response")

    def test_put_city(self):
        city = self.create_unique_city()
        updated_city = {
            "name": f"Updated City {uuid.uuid4()}",
            "country_code": "UY",
        }
        response = self.app.put(
            f"/cities/{city.id}", json=updated_city, headers=self.headers
        )
        self.assertEqual(
            response.status_code,
            200,
            f"Expected status code 200 but got {response.status_code}. Response: {response.json}",
        )
        city_data = response.get_json()
        self.assertEqual(
            city_data["name"],
            updated_city["name"],
            f"Expected updated city name to be {updated_city['name']} but got {city_data['name']}",
        )
        self.assertEqual(
            city_data["country_code"],
            updated_city["country_code"],
            f"Expected updated country code to be {updated_city['country_code']} but got {city_data['country_code']}",
        )
        self.assertIn("id", city_data, "City ID not in response")
        self.assertIn("created_at", city_data, "Created_at not in response")
        self.assertIn("updated_at", city_data, "Updated_at not in response")

    def test_delete_city(self):
        city = self.create_unique_city()
        response = self.app.delete(f"/cities/{city.id}", headers=self.headers)
        self.assertEqual(
            response.status_code,
            204,
            f"Expected status code 204 but got {response.status_code}. Response: {response.text}",
        )

    def test_get_country_cities(self):
        country_code = "UY"  # Use an existing country code for this test
        response = self.app.get(f"/countries/{country_code}/cities")
        self.assertEqual(
            response.status_code,
            200,
            f"Expected status code 200 but got {response.status_code}. Response: {response.json}",
        )
        cities_data = response.get_json()
        self.assertIsInstance(
            cities_data,
            list,
            f"Expected response to be a list but got {type(cities_data)}",
        )


if __name__ == "__main__":
    unittest.main()
