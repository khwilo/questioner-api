'''This module represents tests for the question entity'''
import json

from app.tests.v1.test_base import BaseTestCase

class QuestionTestCase(BaseTestCase):
    '''Test definitions for a question'''
    def test_create_question(self):
        '''Test the API can create a question'''
        res = self.get_response_from_user_login(self.admin_registration, self.admin_login)
        response_msg = json.loads(res.data.decode("UTF-8"))
        access_token = response_msg["access_token"]
        res = self.client().post(
            '/api/v1/meetups',
            headers=self.get_authentication_headers(access_token),
            data=json.dumps(self.meetup)
        )
        self.assertEqual(res.status_code, 201)
        res = self.get_response_from_user_login(self.user_registration, self.user_login)
        response_msg = json.loads(res.data.decode("UTF-8"))
        access_token = response_msg["access_token"]
        res = self.client().post(
            '/api/v1/meetups/1/questions',
            headers=self.get_authentication_headers(access_token),
            data=json.dumps(self.question)
        )
        self.assertEqual(res.status_code, 201)

    def test_ask_non_existent_meetup(self):
        '''Test the API cannot post a question to a non-existent meetup'''
        res = self.get_response_from_user_login(self.admin_registration, self.admin_login)
        response_msg = json.loads(res.data.decode("UTF-8"))
        access_token = response_msg["access_token"]
        res = self.get_response_from_user_login(self.user_registration, self.user_login)
        response_msg = json.loads(res.data.decode("UTF-8"))
        access_token = response_msg["access_token"]
        res = self.client().post(
            '/api/v1/meetups/3/questions',
            headers=self.get_authentication_headers(access_token),
            data=json.dumps(self.question)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 404)
        self.assertEqual(response_msg['message'], "Meetup with id '3' doesn't exist!")

    def test_upvote_question(self):
        '''Test the API can upvote a question'''
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
        res = self.client().patch(
            '/api/v1/meetups/1/questions/1/upvote',
            headers=self.get_authentication_headers(access_token)
        ) # Upvote a question

    def test_downvote_question(self):
        '''Test the API can downvote a question'''
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
        res = self.client().patch(
            '/api/v1/meetups/1/questions/1/downvote',
            headers=self.get_authentication_headers(access_token)
        ) # Downvote a question
        self.assertEqual(res.status_code, 200)
