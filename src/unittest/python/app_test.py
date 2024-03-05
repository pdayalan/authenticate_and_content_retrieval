import unittest
from unittest.mock import patch
from app import app

class TestApp(unittest.TestCase):
    @patch('app.get_user')
    def test_login_success(self, mock_get_user):
        mock_get_user.return_value = {'username': 'test_user', 'password': 'test_password'}
        with app.test_client() as client:
            response = client.post('/login', json={'username': 'test_user', 'password': 'test_password'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['message'], 'Login successful')

    @patch('app.get_user')
    def test_login_failure(self, mock_get_user):
        mock_get_user.return_value = None
        with app.test_client() as client:
            response = client.post('/login', json={'username': 'test_user', 'password': 'test_password'})
            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json['message'], 'Invalid credentials')

    def test_get_content(self):
        with app.test_client() as client:
            response = client.get('/content')
            self.assertEqual(response.status_code, 200)
            self.assertIn('content', response.json)

if __name__ == '__main__':
    unittest.main()
