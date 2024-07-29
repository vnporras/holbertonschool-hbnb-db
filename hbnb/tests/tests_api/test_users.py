import unittest
import uuid

from flask_jwt_extended import create_access_token
from src import create_app, db
from src.models.user import User
from src.config import TestingConfig


class UserManagementTests(unittest.TestCase):

    def setUp(self):
        self.client = create_app(TestingConfig)
        self.app = self.client.test_client()

        self.admin_user = self.create_admin_user()

        with self.client.app_context():
            self.token = create_access_token(
                self.admin_user, additional_claims={"is_admin": True}
            )
            self.headers = {"Authorization": f"Bearer {self.token}"}

    def create_admin_user(self):
        admin_user = User(
            email="riz@lo.tk",
            first_name="Riz",
            last_name="Lo",
            password="password",
            is_admin=True,
        )

        with self.client.app_context():
            db.session.add(admin_user)
            db.session.commit()
            db.session.refresh(admin_user)

        return admin_user

    def create_unique_user(self):
        new_user = User(
            email=f"test.user.{uuid.uuid4()}@example.com",
            password="password",
            first_name="John",
            last_name="Doe",
        )

        with self.client.app_context():
            db.session.add(new_user)
            db.session.commit()
            db.session.refresh(new_user)

        return new_user

    def test_get_users(self):
        response = self.app.get("/users")
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

    def test_post_user(self):
        unique_email = f"test.user.{uuid.uuid4()}@example.com"
        new_user = {
            "email": unique_email,
            "password": "password",
            "first_name": "John",
            "last_name": "Doe",
        }
        response = self.app.post("/users", json=new_user, headers=self.headers)
        self.assertEqual(
            response.status_code,
            201,
            f"Expected status code 201 but got {response.status_code}. Response: {response.json}",
        )
        user_data = response.get_json()
        self.assertEqual(
            user_data["email"],
            new_user["email"],
            f"Expected email to be {new_user['email']} but got {user_data['email']}",
        )
        self.assertEqual(
            user_data["first_name"],
            new_user["first_name"],
            f"Expected first name to be {new_user['first_name']} but got {user_data['first_name']}",
        )
        self.assertEqual(
            user_data["last_name"],
            new_user["last_name"],
            f"Expected last name to be {new_user['last_name']} but got {user_data['last_name']}",
        )
        self.assertIn("id", user_data, "User ID not in response")
        self.assertIn("created_at", user_data, "Created_at not in response")
        self.assertIn("updated_at", user_data, "Updated_at not in response")

    def test_get_user(self):
        user = self.create_unique_user()
        response = self.app.get(f"/users/{user.id}")
        self.assertEqual(
            response.status_code,
            200,
            f"Expected status code 200 but got {response.status_code}. Response: {response.json}",
        )
        user_data = response.get_json()
        self.assertEqual(
            user_data["id"],
            user.id,
            f"Expected user ID to be {user.id} but got {user_data['id']}",
        )
        self.assertIn("email", user_data, "Email not in response")
        self.assertIn("first_name", user_data, "First name not in response")
        self.assertIn("last_name", user_data, "Last name not in response")
        self.assertIn("created_at", user_data, "Created_at not in response")
        self.assertIn("updated_at", user_data, "Updated_at not in response")

    def test_put_user(self):
        user = self.create_unique_user()
        updated_user = {
            "email": f"updated.user.{uuid.uuid4()}@example.com",
            "password": "password",
            "first_name": "John",
            "last_name": "Smith",
        }
        response = self.app.put(
            f"/users/{user.id}", json=updated_user, headers=self.headers
        )
        self.assertEqual(
            response.status_code,
            200,
            f"Expected status code 200 but got {response.status_code}. Response: {response.json}",
        )
        user_data = response.get_json()
        self.assertEqual(
            user_data["email"],
            updated_user["email"],
            f"Expected updated email to be {updated_user['email']} but got {user_data['email']}",
        )
        self.assertEqual(
            user_data["first_name"],
            updated_user["first_name"],
            f"Expected updated first name to be {updated_user['first_name']} but got {user_data['first_name']}",
        )
        self.assertEqual(
            user_data["last_name"],
            updated_user["last_name"],
            f"Expected updated last name to be {updated_user['last_name']} but got {user_data['last_name']}",
        )
        self.assertIn("id", user_data, "User ID not in response")
        self.assertIn("created_at", user_data, "Created_at not in response")
        self.assertIn("updated_at", user_data, "Updated_at not in response")

    def test_delete_user(self):
        user = self.create_unique_user()
        response = self.app.delete(f"/users/{user.id}", headers=self.headers)

        self.assertEqual(
            response.status_code,
            204,
            f"Expected status code 204 but got {response.status_code}. Response: {response.text}",
        )


if __name__ == "__main__":
    unittest.main()
