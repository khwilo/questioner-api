"""This module represents tests for the question entity"""
import json

from app.tests.v2.sample_data import USER_REGISTRATION, USER_LOGIN, QUESTION
from app.tests.v2.test_base import BaseTestCase

class QuestionTestCase(BaseTestCase):
    """Test definitions for a question"""
    def test_ask_non_existent_meetup(self):
        """Test the API cannot post a question to a non-existent meetup"""
        access_token = self.get_access_token(USER_REGISTRATION, USER_LOGIN)
        res = self.client().post(
            '/api/v2/meetups/3/questions',
            headers=self.get_authentication_headers(access_token),
            data=json.dumps(QUESTION)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 404)
        self.assertEqual(response_msg["message"]["error"], "Meetup with id '3' doesn't exist!")

    def test_incorrect_meetup_id(self):
        """Test an incorrect meetup ID is validated"""
        access_token = self.get_access_token(USER_REGISTRATION, USER_LOGIN)
        res = self.client().post(
            '/api/v2/meetups/i/questions',
            headers=self.get_authentication_headers(access_token),
            data=json.dumps(QUESTION)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 400)
        self.assertEqual(response_msg["message"]["error"], "Meetup ID must be an integer value")

    def test_vote_with_incorrect_question_id(self):
        """Test validate question ID on voting"""
        access_token = self.get_access_token(USER_REGISTRATION, USER_LOGIN)
        res = self.client().patch(
            '/api/v2/questions/i/upvote',
            headers=self.get_authentication_headers(access_token)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 400)
        self.assertTrue(response_msg["message"]["error"])
        self.assertEqual(response_msg["message"]["error"], "Question ID must be an integer value")

    def test_vote_on_non_existent_question(self):
        """Test one cannot vote on a non-existent question"""
        access_token = self.get_access_token(USER_REGISTRATION, USER_LOGIN)
        res = self.client().patch(
            '/api/v2/questions/2/upvote',
            headers=self.get_authentication_headers(access_token)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 404)
        self.assertEqual(response_msg["message"]["error"], "Question with ID '2' doesn't exist!")
