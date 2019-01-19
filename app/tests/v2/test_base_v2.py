'''This module represents the base test class for v2 of the API'''
import unittest

from app import create_app
from app.api.v2.models.database import DatabaseSetup

class BaseTestDbTestCase(unittest.TestCase):
    '''Base class for other test classes for API v2'''
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

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

        with self.app.app_context():
            DatabaseSetup.initialize_db()

    def tearDown(self):
        with self.app.app_context():
            DatabaseSetup.destroy()

    def get_accept_content_type_headers(self):
        '''Return the content type headers for the body'''
        content_type = {}
        content_type['Accept'] = 'application/json'
        content_type['Content-Type'] = 'application/json'
        return content_type

    def get_authentication_headers(self, access_token):
        '''Return the authentication header'''
        authentication_headers = self.get_accept_content_type_headers()
        authentication_headers['Authorization'] = "Bearer {}".format(access_token)
        return authentication_headers

if __name__ == "__main__":
    unittest.main()
