'''This module represents the base test class for v2 of the API'''
import unittest

from flask import g
from app import create_app
from app.api.v2.models.base_model import BaseModel
from instance.config import APP_CONFIG
from db import establish_connection, create_tables, drop_tables

class BaseTestDbTestCase(unittest.TestCase):
    '''Base class for other test classes for API v2'''
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app_context.push()

        with self.app.app_context():
            self.database = BaseModel()
            self.connection = establish_connection()
            create_tables(self.connection)

        self.user_registration = dict(
            firstname="test_first",
            lastname="test_last",
            othername="test_other",
            email="tes@example.com",
            phone_number="0700000000",
            username="test_ser",
            is_admin=False,
            password="12345"
        )

    def tearDown(self):
        with self.app.app_context():
            if 'connection' not in g:
                conn = establish_connection()
            drop_tables(conn)

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
