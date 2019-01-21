'''This module represents tests for the user entity'''
import json

from app.tests.v2.test_base_v2 import BaseTestDbTestCase
from app.tests.v2.sample_data import USER_REGISTRATION, USER_DUPLICATE_USERNAME, \
USER_DUPLICATE_EMAIL, USER_LOGIN, ADMIN_LOGIN

class UsersDbTestCase(BaseTestDbTestCase):
    '''Test definitions for a user'''
    def test_db_user_registration(self):
        '''Test a user account can be created in the database'''
        res = self.client().post(
            '/api/v2/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(USER_REGISTRATION)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 201)
        self.assertEqual(response_msg['data'][0]['user']['username'], USER_REGISTRATION['username'])

    def test_duplicate_username(self):
        '''Test a user account with an existing username cannot be created'''
        res = self.client().post(
            '/api/v2/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(USER_REGISTRATION)
        )
        res = self.client().post(
            '/api/v2/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(USER_DUPLICATE_USERNAME)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 409)
        self.assertEqual(response_msg['message'], "Username 'tester_user' already taken!")


    def test_duplicate_email(self):
        '''Test a user account with an existing email address cannot be created'''
        res = self.client().post(
            '/api/v2/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(USER_REGISTRATION)
        )
        res = self.client().post(
            '/api/v2/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(USER_DUPLICATE_EMAIL)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 409)
        self.assertEqual(
            response_msg['message'], "Email address 'tester@example.com' already in use!")

    def test_user_login(self):
        '''Test that a user can login'''
        res = self.client().post(
            '/api/v2/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(USER_REGISTRATION)
        ) # Register a user
        res = self.client().post(
            '/api/v2/auth/login',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(USER_LOGIN)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_msg['data'][0]['message'], "Logged in as 'tester_user'")

    def test_admin_login(self):
        '''Test that an admin can login'''
        res = self.client().post(
            '/api/v2/auth/login',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(ADMIN_LOGIN)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_msg['data'][0]['message'], "Logged in as 'watai'")
