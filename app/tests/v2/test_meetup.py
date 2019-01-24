"""This module represents tests for the meetup entity"""
import json
from app.tests.v2.sample_data import ADMIN_LOGIN, MEETUP, USER_REGISTRATION, \
USER_LOGIN, NEW_MEETUP
from app.tests.v2.test_base import BaseTestCase

class MeetupTestCase(BaseTestCase):
    """Test definitions for a meetup"""
    def test_admin_create_meetup(self):
        """Test an administrator can create a meetup"""
        res = self.client().post(
            '/api/v2/auth/login',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(ADMIN_LOGIN)
        )
        respone_msg = json.loads(res.data.decode("UTF-8"))
        access_token = respone_msg["data"][0]["token"]
        res = self.client().post(
            '/api/v2/meetups',
            headers=self.get_authentication_headers(access_token),
            data=json.dumps(MEETUP)
        )
        self.assertEqual(res.status_code, 201)

    def test_user_cannot_create_meetup(self):
        """Test a regular user cannot create a meetup"""
        access_token = self.get_access_token(USER_REGISTRATION, USER_LOGIN)
        res = self.client().post(
            '/api/v2/meetups',
            headers=self.get_authentication_headers(access_token),
            data=json.dumps(MEETUP)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 403)
        self.assertEqual(
            response_msg["message"]["error"],
            "Only administrators can create a meetup"
        )

    def test_fetch_incorrect_meetup_id(self):
        """Test the API cannot fetch a meetup with an incorrect ID"""
        access_token = self.get_access_token(USER_REGISTRATION, USER_LOGIN)
        res = self.client().get(
            '/api/v2/meetups/i',
            headers=self.get_authentication_headers(access_token)
        )
        self.assertEqual(res.status_code, 400)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"]["error"], "Meetup ID must be an Integer")

    def test_empty_meetup_item(self):
        """Test the API cannot read data from an empty meetup item"""
        access_token = self.get_access_token(USER_REGISTRATION, USER_LOGIN)
        res = self.client().get(
            '/api/v2/meetups/2',
            headers=self.get_authentication_headers(access_token)
        )
        self.assertEqual(res.status_code, 404)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"]["error"], "Meetup with id '2' doesn't exist!")

    def test_fetch_all_meetups(self):
        """Test the API can fetch all meetups"""
        res = self.client().post(
            '/api/v2/auth/login',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(ADMIN_LOGIN)
        )
        respone_msg = json.loads(res.data.decode("UTF-8"))
        access_token = respone_msg["data"][0]["token"]
        self.create_meetup(access_token, MEETUP) # Earlier meetup
        self.create_meetup(access_token, NEW_MEETUP) # Latest meetup
        res = self.client().get(
            '/api/v2/meetups/upcoming/',
            headers=self.get_authentication_headers(access_token)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 200)
        self.assertTrue(response_msg["data"])
        self.assertTrue(respone_msg["data"][0], NEW_MEETUP)

    def test_fetch_empty_meetup_list(self):
        """Test the API cannot fetch data from an empty meetup list data store"""
        access_token = self.get_access_token(USER_REGISTRATION, USER_LOGIN)
        res = self.client().get(
            '/api/v2/meetups/upcoming/',
            headers=self.get_authentication_headers(access_token)
        )
        self.assertEqual(res.status_code, 404)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"]["error"], 'No meetup is available')

    def test_admin_delete_meetup(self):
        """Test the API can delete a meetup record"""
        res = self.client().post(
            '/api/v2/auth/login',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(ADMIN_LOGIN)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        access_token = response_msg["data"][0]["token"]
        res = self.client().delete(
            '/api/v2/meetups/1',
            headers=self.get_authentication_headers(access_token)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"]['error'], "Meetup with ID '1' has been removed!")
