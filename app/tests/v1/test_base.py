'''This module represents the base test class'''
import unittest

from app import create_app
from app.api.v1.models.user_model import USERS

class BaseTestCase(unittest.TestCase):
    '''Base class for other test classes'''
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.user_registration = dict(
            firstname="test_first",
            lastname="test_last",
            othername="test_other",
            email="test@example.com",
            phone_number="0700000000",
            username="test_user",
            is_admin=False,
            password="12345"
        )

    def tearDown(self):
        del USERS[:]
        self.app_context.pop()

    def get_accept_content_type_headers(self):
        '''Return the content type headers for the body'''
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

if __name__ == "__main__":
    unittest.main()
