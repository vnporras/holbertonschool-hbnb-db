import unittest
import uuid

from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token

from src import create_app, db
from src.models.city import City
from src.models.place import Place
from src.models.user import User
from src.config import TestingConfig


class ReviewManagementTests(unittest.TestCase):

    def setUp(self):
        self.client = create_app(TestingConfig)
        self.app = self.client.test_client()
        self.app.testing = True

        self.admin_user = self.create_admin_user()

        with self.client.app_context():
            self.token = create_access_token(self.admin_user)
            self.headers = {"Authorization": f"Bearer {self.token}"}

        self.place = self.create_place()

    def create_user(self):
        user = User(
            email=f"test.user.{uuid.uuid4()}@example.com",
            password="password",
            first_name="John",
            last_name="Doe",
        )

        with self.client.app_context():
            db.session.add(user)
            db.session.commit()
            db.session.refresh(user)

        return user

    def create_admin_user(self):
        user = user = User(
            email=f"test.user.{uuid.uuid4()}@example.com",
            password="password",
            first_name="John",
            last_name="Doe",
            is_admin=True,
        )

        with self.client.app_context():
            db.session.add(user)
            db.session.commit()
            db.session.refresh(user)

        return user

    def create_unique_city(self):
        new_city = City(name=f"Test City {uuid.uuid4()}", country_code="UY")

        with self.client.app_context():
            db.session.add(new_city)
            db.session.commit()
            db.session.refresh(new_city)

        return new_city

    def create_place(self):
        city = self.create_unique_city()
        new_place = {
            "name": "Cozy Cottage",
            "description": "A cozy cottage in the countryside.",
            "address": "123 Country Lane",
            "latitude": 34.052235,
            "longitude": -118.243683,
            "host_id": self.admin_user.id,
            "city_id": city.id,
            "price_per_night": 100,
            "number_of_rooms": 2,
            "number_of_bathrooms": 1,
            "max_guests": 4,
        }

        place = Place(new_place)

        with self.client.app_context():
            db.session.add(place)
            db.session.commit()
            db.session.refresh(place)

        return place

    def test_get_reviews_from_place(self):
        new_review = {
            "place_id": self.place.id,
            "user_id": self.admin_user.id,
            "comment": "Great place to stay!",
            "rating": 5.0,
        }
        response = self.app.post(
            f"/places/{self.place.id}/reviews",
            json=new_review,
            headers=self.headers,
        )
        self.assertEqual(
            response.status_code,
            201,
            f"Expected status code 201 but got {response.status_code}. Response: {response.json}",
        )

        review_id = response.get_json()["id"]

        response = self.app.get(f"/places/{self.place.id}/reviews")
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
        self.assertTrue(
            any(review["id"] == review_id for review in response.get_json()),
            f"Expected review with ID {review_id} to be in response but it wasn't",
        )

    def test_get_reviews_from_user(self):
        new_review = {
            "place_id": self.place.id,
            "user_id": self.admin_user.id,
            "comment": "Great place to stay!",
            "rating": 5.0,
        }
        response = self.app.post(
            f"/places/{self.place.id}/reviews",
            json=new_review,
            headers=self.headers,
        )
        self.assertEqual(
            response.status_code,
            201,
            f"Expected status code 201 but got {response.status_code}. Response: {response.json}",
        )

        review_id = response.get_json()["id"]

        response = self.app.get(
            f"/users/{self.admin_user.id}/reviews",
            headers=self.headers,
        )
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
        self.assertTrue(
            any(review["id"] == review_id for review in response.get_json()),
            f"Expected review with ID {review_id} to be in response but it wasn't",
        )

    def test_post_review(self):
        new_review = {
            "user_id": self.admin_user.id,
            "comment": "This place is amazing!",
            "rating": 4.5,
        }
        response = self.app.post(
            f"/places/{self.place.id}/reviews",
            json=new_review,
            headers=self.headers,
        )
        self.assertEqual(
            response.status_code,
            201,
            f"Expected status code 201 but got {response.status_code}. Response: {response.json}",
        )
        review_data = response.get_json()
        for key in new_review:
            self.assertEqual(
                review_data[key],
                new_review[key],
                f"Expected {key} to be {new_review[key]} but got {review_data[key]}",
            )
        self.assertIn("id", review_data, "Review ID not in response")
        self.assertIn("created_at", review_data, "Created_at not in response")
        self.assertIn("updated_at", review_data, "Updated_at not in response")
        self.review_id = review_data["id"]  # Store review ID for further tests

    def test_get_review(self):
        self.test_post_review()  # Ensure a review is created
        response = self.app.get(f"/reviews/{self.review_id}")
        self.assertEqual(
            response.status_code,
            200,
            f"Expected status code 200 but got {response.status_code}. Response: {response.json}",
        )
        review_data = response.get_json()
        new_review = {
            "user_id": self.admin_user.id,
            "comment": "This place is amazing!",
            "rating": 4.5,
        }
        for key in new_review:
            self.assertEqual(
                review_data[key],
                new_review[key],
                f"Expected {key} to be {new_review[key]} but got {review_data[key]}",
            )
        self.assertIn("id", review_data, "Review ID not in response")
        self.assertIn("created_at", review_data, "Created_at not in response")
        self.assertIn("updated_at", review_data, "Updated_at not in response")

    def test_put_review(self):
        self.test_post_review()  # Ensure a review is created
        updated_review = {
            "place_id": self.place.id,
            "user_id": self.admin_user.id,
            "comment": "Amazing place, had a great time!",
            "rating": 4.8,
        }
        response = self.app.put(
            f"/reviews/{self.review_id}",
            json=updated_review,
            headers=self.headers,
        )
        self.assertEqual(
            response.status_code,
            200,
            f"Expected status code 200 but got {response.status_code}. Response: {response.json}",
        )
        review_data = response.get_json()
        for key in updated_review:
            self.assertEqual(
                review_data[key],
                updated_review[key],
                f"Expected updated {key} to be {updated_review[key]} but got {review_data[key]}",
            )
        self.assertIn("id", review_data, "Review ID not in response")
        self.assertIn("created_at", review_data, "Created_at not in response")
        self.assertIn("updated_at", review_data, "Updated_at not in response")

    def test_delete_review(self):
        self.test_post_review()  # Ensure a review is created
        response = self.app.delete(
            f"/reviews/{self.review_id}",
            headers=self.headers,
        )
        self.assertEqual(
            response.status_code,
            204,
            f"Expected status code 204 but got {response.status_code}. Response: {response.text}",
        )


if __name__ == "__main__":
    unittest.main()
