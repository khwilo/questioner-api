'''This module represents tests for the user entity'''
import json

from app.tests.v2.test_base import BaseTestCase
from app.tests.v2.sample_data import USER_REGISTRATION, USER_DUPLICATE_USERNAME, \
USER_DUPLICATE_EMAIL, USER_DIGIT_USERNAME, USER_EMPTY_USERNAME, USER_EMPTY_PASSWORD, \
USER_WRONG_EMAIL_FORMAT, USER_LOGIN, ADMIN_LOGIN, USER_LOGIN_INCORRECT_PASSWORD

class UserTestCase(BaseTestCase):
    '''Test definitions for a user'''
    def test_user_registration(self):
        '''Test the API can register a user'''
        res = self.client().post(
            '/api/v2/auth/signup',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(USER_REGISTRATION)
        )
        self.assertEqual(res.status_code, 201)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(response_msg["status"], 201)
        self.assertTrue(response_msg["data"][0]["message"])
        self.assertEqual(
            response_msg["data"][0]["message"],
            "User account created successfully"
        )

    def test_digit_username(self):
        '''
        Test the API cannot register a user with a username consisting of digits only
        '''
        res = self.client().post(
            '/api/v2/auth/signup',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(USER_DIGIT_USERNAME)
        )
        self.assertEqual(res.status_code, 400)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"]["error"], "username cannot consist of digits only")

    def test_empty_username(self):
        '''
        Test the API cannot register a user with an empty username
        '''
        res = self.client().post(
            '/api/v2/auth/signup',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(USER_EMPTY_USERNAME)
        )
        self.assertEqual(res.status_code, 400)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"]["error"], "username cannot be empty")

    def test_empty_password(self):
        '''
        Test the API cannot register a user without a password
        '''
        res = self.client().post(
            '/api/v2/auth/signup',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(USER_EMPTY_PASSWORD)
        )
        self.assertEqual(res.status_code, 400)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"]["error"], "password cannot be empty")

    def test_invalid_email_address_registration(self):
        '''
        Test the API cannot register a user with an invalid email address
        '''
        res = self.client().post(
            '/api/v2/auth/signup',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(USER_WRONG_EMAIL_FORMAT)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 400)
        self.assertEqual(
            response_msg["message"]["error"],
            "The email address is not valid. It must have exactly one @-sign."
        )

    def test_duplicate_username(self):
        '''Test a user account with an existing username cannot be created'''
        res = self.client().post(
            '/api/v2/auth/signup',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(USER_REGISTRATION)
        )
        res = self.client().post(
            '/api/v2/auth/signup',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(USER_DUPLICATE_USERNAME)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 409)
        self.assertEqual(response_msg['message'], "Username 'tester_user' already taken!")

    def test_duplicate_email(self):
        '''Test a user account with an existing email address cannot be created'''
        res = self.client().post(
            '/api/v2/auth/signup',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(USER_REGISTRATION)
        )
        res = self.client().post(
            '/api/v2/auth/signup',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(USER_DUPLICATE_EMAIL)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 409)
        self.assertEqual(
            response_msg['message'], "Email address 'tester@example.com' already in use!")

    def test_user_login(self):
        '''Test the API can log in a user'''
        res = self.client().post(
            '/api/v2/auth/signup',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(USER_REGISTRATION)
        )
        self.assertEqual(res.status_code, 201)
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

    def test_incorrect_login(self):
        '''Test the API cannot log in a user who is not yet registered'''
        res = self.client().post(
            '/api/v2/auth/login',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(USER_LOGIN)
        )
        self.assertEqual(res.status_code, 404)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(
            response_msg["message"]["error"],
            "User with username 'tester_user' doesn't exist!"
        )

    def test_incorrect_password(self):
        '''Test the API cannot log in a user with an incorrect password'''
        res = self.client().post(
            '/api/v2/auth/signup',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(USER_REGISTRATION)
        )
        self.assertEqual(res.status_code, 201)
        res = self.client().post(
            '/api/v2/auth/login',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(USER_LOGIN_INCORRECT_PASSWORD)
        )
        self.assertEqual(res.status_code, 401)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"]["error"], "The password you entered doesn't match")
