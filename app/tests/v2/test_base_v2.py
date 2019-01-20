'''This module represents the base test class for v2 of the API'''
import unittest

from app import create_app
from db import establish_connection, destroy

class BaseTestDbTestCase(unittest.TestCase):
    '''Base class for other test classes for API v2'''
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()

        self.client = self.app.test_client

        with self.app_context:
            establish_connection()

    def tearDown(self):
        with self.app_context:
            destroy()

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
