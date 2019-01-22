'''This module represents tests for the rsvp entity'''
import json

from app.tests.v2.test_base import BaseTestCase

class RsvpTestCase(BaseTestCase):
    '''Test definitions for an rsvp'''
    def test_respond_meetup_rsvp(self):
        '''Test the API can respond to a meetup rsvp'''
        access_token = self.get_access_token(self.admin_registration, self.admin_login)
        self.create_meetup(access_token, self.meetup)
        access_token = self.get_access_token(self.user_registration, self.user_login)
        self.create_question(access_token, self.question)
        res = self.client().post(
            '/api/v1/meetups/1/rsvps',
            headers=self.get_authentication_headers(access_token),
            data=json.dumps(self.rsvp)
        ) # respond to a meetup rsvp
        self.assertEqual(res.status_code, 201)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(response_msg['data'][0]['status'], "maybe")
