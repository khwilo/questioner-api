'''This module represents tests for the meetup entity'''
import json

from app.api.v2.models.meetup_model import MEETUPS
from app.tests.v2.test_base import BaseTestCase

class MeetupTestCase(BaseTestCase):
    '''Test definitions for a meetup'''
    def test_admin_create_meetup(self):
        '''Test an administrator can create a meetup'''
        access_token = self.get_access_token(self.admin_registration, self.admin_login)
        res = self.client().post(
            '/api/v2/meetups',
            headers=self.get_authentication_headers(access_token),
            data=json.dumps(self.meetup)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 201)
        self.assertTrue(response_msg['data'])
        self.assertEqual(MEETUPS[0], response_msg['data'][0])

    def test_user_cannot_create_meetup(self):
        '''Test a regular user cannot create a meetup'''
        access_token = self.get_access_token(self.user_registration, self.user_login)
        res = self.client().post(
            '/api/v2/meetups',
            headers=self.get_authentication_headers(access_token),
            data=json.dumps(self.meetup)
        )
        self.assertEqual(res.status_code, 403)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"]["error"], "Only administrators can create a meetup")

    def test_fetch_one_meetup(self):
        '''Test the API can fetch one meetup'''
        access_token = self.get_access_token(self.admin_registration, self.admin_login)
        self.create_meetup(access_token, self.meetup)
        self.create_meetup(access_token, self.new_meetup)
        res = self.client().get(
            '/api/v2/meetups/2',
            headers=self.get_authentication_headers(access_token)
        )
        self.assertEqual(res.status_code, 200)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(response_msg["status"], 200)
        self.assertTrue(response_msg["data"])
        self.assertEqual(MEETUPS[1], response_msg['data'][0])

    def test_fetch_incorrect_meetup_id(self):
        '''Test the API cannot fetch a meetup with an incorrect ID'''
        access_token = self.get_access_token(self.admin_registration, self.admin_login)
        self.create_meetup(access_token, self.meetup)
        res = self.client().get(
            '/api/v2/meetups/i',
            headers=self.get_authentication_headers(access_token)
        )
        self.assertEqual(res.status_code, 400)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"]["error"], "Meetup ID must be an Integer")

    def test_empty_meetup_item(self):
        '''Test the API cannot read data from an empty meetup item'''
        access_token = self.get_access_token(self.admin_registration, self.admin_login)
        res = self.client().get(
            '/api/v2/meetups/2',
            headers=self.get_authentication_headers(access_token)
        )
        self.assertEqual(res.status_code, 404)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"]["error"], "Meetup with id '2' doesn't exist!")

    def test_fetch_all_meetups(self):
        '''Test the API can fetch all meetups'''
        access_token = self.get_access_token(self.admin_registration, self.admin_login)
        self.create_meetup(access_token, self.meetup) # Earlier meetup
        self.create_meetup(access_token, self.new_meetup) # Latest meetup
        res = self.client().get(
            '/api/v2/meetups/upcoming/',
            headers=self.get_authentication_headers(access_token)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 200)
        self.assertTrue(response_msg['data'])
        self.assertEqual(
            MEETUPS[1],
            response_msg['data'][0]
        ) # Assert that the latest meetup is always displayed first

    def test_fetch_empty_meetup_list(self):
        '''Test the API cannot fetch data from an empty meetup list data store'''
        access_token = self.get_access_token(self.admin_registration, self.admin_login)
        res = self.client().get(
            '/api/v2/meetups/upcoming/',
            headers=self.get_authentication_headers(access_token)
        )
        self.assertEqual(res.status_code, 404)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"]["error"], 'No meetup is available')
