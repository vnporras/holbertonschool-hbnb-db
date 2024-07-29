import unittest
from src import create_app
from src.config import TestingConfig


class CountryManagementTests(unittest.TestCase):

    def setUp(self):
        self.client = create_app(TestingConfig)
        self.app = self.client.test_client()
        self.app.testing = True

    def test_get_countries(self):
        response = self.app.get("/countries")
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

    def test_get_country(self):
        country_code = "UY"  # Use an existing country code for this test
        response = self.app.get(f"/countries/{country_code}")
        self.assertEqual(
            response.status_code,
            200,
            f"Expected status code 200 but got {response.status_code}. Response: {response.json}",
        )
        country_data = response.get_json()
        self.assertEqual(
            country_data["code"],
            country_code,
            f"Expected country code to be {country_code} but got {country_data['code']}",
        )
        self.assertIn("name", country_data, "Name not in response")


if __name__ == "__main__":
    unittest.main()
