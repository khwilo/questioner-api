'''This module represents the base test class'''
import json
import unittest

from app import create_app
from db import establish_connection, destroy

class BaseTestCase(unittest.TestCase):
    '''Base class for other test classes'''
    def setUp(self):
        self.app = create_app(config_name="testing")
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

    def get_access_token(self, user_registration, user_login):
        '''Fetch access token from user login'''
        self.client().post(
            '/api/v2/auth/signup',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(user_registration)
        ) # User Registration
        res = self.client().post(
            '/api/v2/auth/login',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(user_login)
        ) # User Log In
        response_msg = json.loads(res.data.decode("UTF-8"))
        access_token = response_msg["data"][0]["token"]
        return access_token

    def create_meetup(self, access_token, meetup):
        '''Create a meetup record'''
        self.client().post(
            '/api/v2/meetups',
            headers=self.get_authentication_headers(access_token),
            data=json.dumps(meetup)
        )

    def create_question(self, access_token, question):
        '''Create a question record'''
        self.client().post(
            '/api/v2/meetups/1/questions',
            headers=self.get_authentication_headers(access_token),
            data=json.dumps(question)
        )

if __name__ == "__main__":
    unittest.main()
