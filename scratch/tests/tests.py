"""
Tests
"""
import json
import unittest

import sqlalchemy.exc

from scratch.database.models import Users
from app import app as test_app
import app

app.initialize_app(test_app)


class UnitTestCase(unittest.TestCase):
    def test_valid_create_response(self):
        """
        Test valid create_response in scratch.api.utils
        """
        user = Users(2, "John Doe")
        self.assertEqual("John Doe", user.name)
        self.assertEqual(2, user.id)

    def test_invalid_create_response(self):
        """
        Test invalid create_response in scratch.api.utils
        """
        user = Users(2, "John Doe")
        self.assertNotEqual("John Dow", user.name)
        self.assertNotEqual(21, user.id)


class BlueprintTestCase(unittest.TestCase):

    def setUp(self):
        """
        app setup
        """
        test_app.testing = True
        self.client_test = test_app.test_client()

    def test_valid_get_user(self):
        """
        Test valid get user /v1/users in app.py
        """
        result = self.client_test.get('v1/users/')
        response = json.loads(result.data)
        self.assertEqual(response['Users'][0]['name'], 'Foo Barrington', 'valid name')
        self.assertEqual(response['Users'][0]['id'], 1, 'valid id')
        self.assertEqual(response['Users'][1]['name'], 'Jane Doerty', 'valid name')
        self.assertEqual(response['Users'][1]['id'], 2, 'valid id')
        self.assertEqual(200, result.status_code)

    def test_valid_post_user(self):
        """
        Test valid post user /v1/users in app.py
        """
        result = self.client_test.post('v1/users/', json={'name': 'John Doe'})
        response = json.loads(result.data)
        self.assertEqual(response['name'], 'John Doe', 'valid name')
        self.assertTrue(response.get('id', -1) != -1)
        self.assertEqual(200, result.status_code)

    def test_valid_get_user_by_id(self):
        """
        Test valid get user by id /v1/users/1 in app.py
        """
        result = self.client_test.get('v1/users/1')
        response = json.loads(result.data)
        self.assertEqual(response['name'], 'Foo Barrington', 'valid name')
        self.assertEqual(response['id'], 1, 'valid id')
        self.assertEqual(200, result.status_code)

    def test_invalid_get_user(self):
        """
        Test valid get user /v1/users in app.py
        """
        result = self.client_test.get('v1/user/')
        self.assertEqual(404, result.status_code)

    def test_invalid_post_user(self):
        """
        Test valid get user /v1/users in app.py
        """
        result = self.client_test.post('v1/user/1')
        self.assertEqual(404, result.status_code)

    def test_invalid_post_user(self):
        """
        Test valid get user /v1/users in app.py
        """
        result = self.client_test.post('v1/user/1')
        self.assertEqual(404, result.status_code)

    def test_invalid_get_user_does_not_exist(self):
        """
        Test valid get user /v1/users in app.py
        """
        with self.assertRaises(sqlalchemy.exc.NoResultFound):
            result = self.client_test.get('v1/users/111111111111')
            response = json.loads(result.data)
            self.assertEqual(404, result.status_code)
            self.assertTrue(response['message'])


if __name__ == '__main__':
    unittest.main()
