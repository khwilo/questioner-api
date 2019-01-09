'''This module represents tests for the meetup entity'''
import json

from app.tests.v1.test_base import BaseTestCase

class MeetupTestCase(BaseTestCase):
    '''Test definitions for a meetup'''
    def test_admin_create_meetup(self):
        '''Test an administrator can create a meetup'''
        res = self.get_response_from_user_login(self.admin_registration, self.admin_login)
        response_msg = json.loads(res.data.decode("UTF-8"))
        access_token = response_msg["access_token"]
        res = self.client().post(
            '/api/v1/meetups',
            headers=self.get_authentication_headers(access_token),
            data=json.dumps(self.meetup)
        )
        self.assertEqual(res.status_code, 201)

    def test_user_cannot_create_meetup(self):
        '''Test a regular user cannot create a meetup'''
        res = self.get_response_from_user_login(self.user_registration, self.user_login)
        response_msg = json.loads(res.data.decode("UTF-8"))
        access_token = response_msg["access_token"]
        res = self.client().post(
            '/api/v1/meetups',
            headers=self.get_authentication_headers(access_token),
            data=json.dumps(self.meetup)
        )
        self.assertEqual(res.status_code, 401)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(response_msg['message'], "Only administrators can create a meetup")
