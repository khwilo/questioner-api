'''This module represents tests for the question entity'''
import json

from app.api.v2.models.meetup_model import MEETUPS
from app.tests.v2.test_base import BaseTestCase

class QuestionTestCase(BaseTestCase):
    '''Test definitions for a question'''
    def test_create_question(self):
        '''Test the API can create a question'''
        access_token = self.get_access_token(self.admin_registration, self.admin_login)
        self.create_meetup(access_token, self.meetup)
        access_token = self.get_access_token(self.user_registration, self.user_login)
        res = self.client().post(
            '/api/v1/meetups/1/questions',
            headers=self.get_authentication_headers(access_token),
            data=json.dumps(self.question)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 201)
        self.assertTrue(response_msg['data'])
        self.assertEqual(
            MEETUPS[0]['questions'][0]['question_id'],
            response_msg['data'][0]['questions'][0]['question_id']
        )

    def test_ask_non_existent_meetup(self):
        '''Test the API cannot post a question to a non-existent meetup'''
        access_token = self.get_access_token(self.user_registration, self.user_login)
        res = self.client().post(
            '/api/v1/meetups/3/questions',
            headers=self.get_authentication_headers(access_token),
            data=json.dumps(self.question)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 404)
        self.assertEqual(response_msg["message"]["error"], "Meetup with id '3' doesn't exist!")

    def test_upvote_question(self):
        '''Test the API can upvote a question'''
        access_token = self.get_access_token(self.admin_registration, self.admin_login)
        self.create_meetup(access_token, self.meetup)
        access_token = self.get_access_token(self.user_registration, self.user_login)
        self.create_question(access_token, self.question)
        res = self.client().patch(
            '/api/v1/meetups/1/questions/1/upvote',
            headers=self.get_authentication_headers(access_token)
        ) # Upvote a question
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 200)
        self.assertTrue(response_msg['data'])
        self.assertEqual(response_msg['data'][0]['votes'], 1)

    def test_downvote_question(self):
        '''Test the API can downvote a question'''
        access_token = self.get_access_token(self.admin_registration, self.admin_login)
        self.create_meetup(access_token, self.meetup)
        access_token = self.get_access_token(self.user_registration, self.user_login)
        self.create_question(access_token, self.question)
        res = self.client().patch(
            '/api/v1/meetups/1/questions/1/downvote',
            headers=self.get_authentication_headers(access_token)
        ) # Downvote a question
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 200)
        self.assertTrue(response_msg['data'])
        self.assertEqual(response_msg['data'][0]['votes'], -1)
