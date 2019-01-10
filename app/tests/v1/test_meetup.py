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

    def test_fetch_one_meetup(self):
        '''Test the API can fetch one meetup'''
        res = self.get_response_from_user_login(self.admin_registration, self.admin_login)
        response_msg = json.loads(res.data.decode("UTF-8"))
        access_token = response_msg["access_token"]
        res = self.client().post(
            '/api/v1/meetups',
            headers=self.get_authentication_headers(access_token),
            data=json.dumps(self.meetup)
        )
        self.assertEqual(res.status_code, 201)
        res = self.client().get(
            '/api/v1/meetups/1',
            headers=self.get_authentication_headers(access_token)
        )
        self.assertEqual(res.status_code, 200)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(response_msg["status"], 200)
        self.assertTrue(response_msg["data"])

    def test_incorrect_meetup_id(self):
        '''Test the API cannot fetch a meetup with an incorrect ID'''
        res = self.get_response_from_user_login(self.admin_registration, self.admin_login)
        response_msg = json.loads(res.data.decode("UTF-8"))
        access_token = response_msg["access_token"]
        res = self.client().post(
            '/api/v1/meetups',
            headers=self.get_authentication_headers(access_token),
            data=json.dumps(self.meetup)
        )
        self.assertEqual(res.status_code, 201)
        res = self.client().get(
            '/api/v1/meetups/i',
            headers=self.get_authentication_headers(access_token)
        )
        self.assertEqual(res.status_code, 400)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"], "Meetup ID must be an Integer")

    def test_empty_meetup_item(self):
        '''Test the API cannot read data from an empty meetup item'''
        res = self.get_response_from_user_login(self.admin_registration, self.admin_login)
        response_msg = json.loads(res.data.decode("UTF-8"))
        access_token = response_msg["access_token"]
        res = self.client().get(
            '/api/v1/meetups/2',
            headers=self.get_authentication_headers(access_token)
        )
        self.assertEqual(res.status_code, 404)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"], "Meetup with id '2' doesn't exist!")

    def test_fetch_all_meetups(self):
        '''Test the API can fetch all meetups'''
        res = self.get_response_from_user_login(self.admin_registration, self.admin_login)
        response_msg = json.loads(res.data.decode("UTF-8"))
        access_token = response_msg["access_token"]
        res = self.client().post(
            '/api/v1/meetups',
            headers=self.get_authentication_headers(access_token),
            data=json.dumps(self.meetup)
        )
        self.assertEqual(res.status_code, 201)
        res = self.client().get(
            '/api/v1/meetups/upcoming/',
            headers=self.get_authentication_headers(access_token)
        )
        self.assertEqual(res.status_code, 200)

    def test_fetch_empty_meetup_list(self):
        '''Test the API cannot fetch data from an empty meetup list data store'''
        res = self.get_response_from_user_login(self.admin_registration, self.admin_login)
        response_msg = json.loads(res.data.decode("UTF-8"))
        access_token = response_msg["access_token"]
        res = self.client().get(
            '/api/v1/meetups/upcoming/',
            headers=self.get_authentication_headers(access_token)
        )
        self.assertEqual(res.status_code, 404)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(response_msg['message'], 'No meetup is available')
