import unittest
import app
create_app = app.create_app


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()

    def test_create_user(self):
        response = self.client.post(
            "/api/v1/users/",
            json={
                "first_name": "Test",
                "last_name": "User",
                "email": "test@example.com",
                "password": "123456"
            }
        )
        self.assertIn(response.status_code, [200, 201])

    def test_protected_route_without_token(self):
        response = self.client.post("/api/v1/places/", json={})
        self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()

