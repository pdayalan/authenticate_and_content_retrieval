import unittest
import json
from src.main.python import app

class TestUserEndpoint(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_create_user(self):
        # Define the request payload
        payload = {
            "username": "auppal",
            "password": "admin"
        }

        # Make a POST request to the /users endpoint
        response = self.app.post('/users', 
                                 data=json.dumps(payload),
                                 content_type='application/json')

        # Assert the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert the response data contains the expected message
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'User created successfully')

if __name__ == '__main__':
    unittest.main()
