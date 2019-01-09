'''This module represents tests for the user entity'''
import json

from app.api.v1.models.user_model import USERS, UserModel
from app.tests.v1.test_base import BaseTestCase

class UserTestCase(BaseTestCase):
    '''Test definitions for a user'''
    def test_user_registration(self):
        '''Test the API can register a user'''
        res = self.client().post(
            '/auth/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(self.user_registration)
        )
        self.assertEqual(res.status_code, 201)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(response_msg["status"], 201)
        self.assertTrue(response_msg["data"][0]["message"])
        self.assertEqual(response_msg["data"][0]["message"], "Create a user record")

    def test_digit_username(self):
        '''
        Test the API cannot register a user with a username consisting of digits only
        '''
        res = self.client().post(
            '/auth/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(self.digit_username)
        )
        self.assertEqual(res.status_code, 400)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"], "username cannot consist of digits only")

    def test_empty_username(self):
        '''
        Test the API cannot register a user with an empty username
        '''
        res = self.client().post(
            '/auth/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(self.empty_username)
        )
        self.assertEqual(res.status_code, 400)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"], "username cannot be empty")

    def test_empty_password(self):
        '''
        Test the API cannot register a user without a password
        '''
        res = self.client().post(
            '/auth/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(self.empty_password)
        )
        self.assertEqual(res.status_code, 400)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"], "password cannot be empty")

    def test_duplicate_user_registration(self):
        '''
        Test the API can register a user only once
        '''
        res = self.client().post(
            '/auth/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(self.user_registration)
        ) # First user registration
        self.assertEqual(res.status_code, 201)
        res = self.client().post(
            '/auth/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(self.user_registration)
        ) # Second user registration
        self.assertEqual(res.status_code, 401)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(
            response_msg["message"],
            "A user with username 'test_user' already exists!"
        )

    def test_user_login(self):
        '''Test the API can log in a user'''
        res = self.client().post(
            '/auth/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(self.user_registration)
        )
        self.assertEqual(res.status_code, 201)
        res = self.client().post(
            '/auth/login',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(self.user_login)
        )
        self.assertEqual(res.status_code, 200)

    def test_get_user_by_username(self):
        '''Test the method fetch a user by user username returns the correct user'''
        self.client().post(
            '/auth/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(self.user_registration)
        )
        self.assertEqual(UserModel.get_user_by_username('test_user'), USERS[0])
