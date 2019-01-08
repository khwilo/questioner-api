'''This module represents the base test class'''
import json
import unittest

from app import create_app

class BaseTestCase(unittest.TestCase):
    '''Base class for other test classes'''
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_welcome_message(self):
        '''Test the API can return the welcome message'''
        res = self.client().get("/")
        self.assertEqual(res.status_code, 200)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual("Welcome to Questioner", response_msg["message"])

if __name__ == "__main__":
    unittest.main()
