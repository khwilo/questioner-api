'''This module represents tests for the meetup entity'''
import json

from app.tests.v1.test_base import BaseTestCase

class MeetupTestCase(BaseTestCase):
    '''Test definitions for a meetup'''
    def test_user_post_meetup(self):
        '''Test the API can create a meetup'''
        res = self.get_response_from_user_login(self.adming_registration, self.admin_login)
        response_msg = json.loads(res.data.decode("UTF-8"))
        access_token = response_msg["access_token"]
        res = self.client().post(
            '/api/v1/meetups',
            headers=self.get_authentication_headers(access_token),
            data=json.dumps(self.meetup)
        )
        self.assertEqual(res.status_code, 201)
