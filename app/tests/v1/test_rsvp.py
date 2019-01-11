'''This module represents tests for the rsvp entity'''
import json

from app.tests.v1.test_base import BaseTestCase

class RsvpTestCase(BaseTestCase):
    '''Test definitions for an rsvp'''
    def test_respond_meetup_rsvp(self):
        '''Test the API can respond to a meetup rsvp'''
        res = self.get_response_from_user_login(self.admin_registration, self.admin_login)
        response_msg = json.loads(res.data.decode("UTF-8"))
        access_token = response_msg["access_token"]
        res = self.client().post(
            '/api/v1/meetups',
            headers=self.get_authentication_headers(access_token),
            data=json.dumps(self.meetup)
        ) # Create a meetup
        self.assertEqual(res.status_code, 201)
        res = self.get_response_from_user_login(self.user_registration, self.user_login)
        response_msg = json.loads(res.data.decode("UTF-8"))
        access_token = response_msg["access_token"]
        res = self.client().post(
            '/api/v1/meetups/1/questions',
            headers=self.get_authentication_headers(access_token),
            data=json.dumps(self.question)
        ) # Create a question
        self.assertEqual(res.status_code, 201)
        res = self.client().post(
            '/api/v1/meetups/1/rsvps',
            headers=self.get_authentication_headers(access_token),
            data=json.dumps(self.rsvp)
        ) # respond to a meetup rsvp
        self.assertEqual(res.status_code, 201)
