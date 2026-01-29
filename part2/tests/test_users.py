import unittest
from hbnb.app import create_app


class TestUserEndpoints(unittest.TestCase):

	    def setUp(self):
	    app = create_app()
	    app.testing = True
	    self.client = app.test_client()

	def test_create_user(self):
	    response = self.client.post(
	        "/api/v1/users/",
	        json={
	            "first_name": "Test",
                "last_name": "User",
	            "email": "test@example.com",
	            "password": "password123"
                }
            )
            self.assertIn(response.status_code, [200, 201])

    def test_get_user_not_found(self):
	    response = self.client.get("/api/v1/users/does-not-exist")
	    self.assertIn(response.status_code, [404, 400])


if __name__ == "__main__":
	unittest.main()
