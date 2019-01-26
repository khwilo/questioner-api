"""This module represents tests for the rsvp entity"""
import json

from app.tests.v2.sample_data import ADMIN_LOGIN, MEETUP, RSVP, \
USER_REGISTRATION, USER_LOGIN
from app.tests.v2.test_base import BaseTestCase

class RsvpTestCase(BaseTestCase):
    """Test definitions for an rsvp"""
    def test_respond_meetup_rsvp(self):
        """Test the API can respond to a meetup rsvp"""
        res = self.client().post(
            '/api/v2/auth/login',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(ADMIN_LOGIN)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        access_token = response_msg["data"][0]["token"]
        self.create_meetup(access_token, MEETUP)
        access_token = self.get_access_token(USER_REGISTRATION, USER_LOGIN)
        res = self.client().post(
            '/api/v2/meetups/1/rsvps',
            headers=self.get_authentication_headers(access_token),
            data=json.dumps(RSVP)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 201)
        self.assertEqual(response_msg["data"][0]["status"], "maybe")

    def test_respond_meetup_rsvp_with_wrong_meetup_id(self):
        """Test the API can validate a meetup ID"""
        access_token = self.get_access_token(USER_REGISTRATION, USER_LOGIN)
        res = self.client().post(
            '/api/v2/meetups/c/rsvps',
            headers=self.get_authentication_headers(access_token),
            data=json.dumps(RSVP)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 400)
        self.assertEqual(response_msg["message"]["error"], "Meetup ID must be an integer value")

    def test_rsvp_to_non_existent_meetup(self):
        """Test that a user cannot RSVP to a non-existent meetup"""
        access_token = self.get_access_token(USER_REGISTRATION, USER_LOGIN)
        res = self.client().post(
            '/api/v2/meetups/41/rsvps',
            headers=self.get_authentication_headers(access_token),
            data=json.dumps(RSVP)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 404)
        self.assertEqual(response_msg["message"]["error"], "Meetup with id '41' doesn't exist!")
