"""This module represents tests for the question entity"""
import json

from app.tests.v2.sample_data import USER_REGISTRATION, USER_LOGIN, QUESTION, \
ADMIN_LOGIN, MEETUP, NEW_USER_REGISTRATION, NEW_USER_LOGIN
from app.tests.v2.test_base import BaseTestCase

class QuestionTestCase(BaseTestCase):
    """Test definitions for a question"""
    def test_ask_question_meetup(self):
        """Test the API can post a question to a meetup"""
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
            '/api/v2/meetups/1/questions',
            headers=self.get_authentication_headers(access_token),
            data=json.dumps(QUESTION)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 201)
        self.assertEqual(response_msg["message"], "Question created successfully!")


    def test_ask_question_non_existent_meetup(self):
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

    def test_ask_question_incorrect_meetup_id(self):
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

    def test_upvote_question(self):
        """Test the API can upvote a question"""
        res = self.client().post(
            '/api/v2/auth/login',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(ADMIN_LOGIN)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        access_token = response_msg["data"][0]["token"]
        self.create_meetup(access_token, MEETUP)
        access_token = self.get_access_token(USER_REGISTRATION, USER_LOGIN)
        self.create_question(access_token, QUESTION)
        access_token = self.get_access_token(NEW_USER_REGISTRATION, NEW_USER_LOGIN)
        res = self.client().patch(
            '/api/v2/questions/1/upvote',
            headers=self.get_authentication_headers(access_token)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_msg["data"][0]["votes"], 1)

    def test_downvote_question(self):
        """Test the API can downvote a question"""
        res = self.client().post(
            '/api/v2/auth/login',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(ADMIN_LOGIN)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        access_token = response_msg["data"][0]["token"]
        self.create_meetup(access_token, MEETUP)
        access_token = self.get_access_token(USER_REGISTRATION, USER_LOGIN)
        self.create_question(access_token, QUESTION)
        access_token = self.get_access_token(NEW_USER_REGISTRATION, NEW_USER_LOGIN)
        res = self.client().patch(
            '/api/v2/questions/1/downvote',
            headers=self.get_authentication_headers(access_token)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_msg["data"][0]["votes"], -1)

    def test_wrong_vote_parameter(self):
        """Test the API can validate if a vote is either an upvote/downvote"""
        res = self.client().post(
            '/api/v2/auth/login',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(ADMIN_LOGIN)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        access_token = response_msg["data"][0]["token"]
        self.create_meetup(access_token, MEETUP)
        access_token = self.get_access_token(USER_REGISTRATION, USER_LOGIN)
        self.create_question(access_token, QUESTION)
        access_token = self.get_access_token(NEW_USER_REGISTRATION, NEW_USER_LOGIN)
        res = self.client().patch(
            '/api/v2/questions/1/vote',
            headers=self.get_authentication_headers(access_token)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 400)
        self.assertEqual(
            response_msg["message"]["error"],
            "Vote path parameter can either be upvote / downvote"
        )

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

    def test_a_user_can_vote_once(self):
        """Test that a user can only vote once for a question"""
        res = self.client().post(
            '/api/v2/auth/login',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(ADMIN_LOGIN)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        access_token = response_msg["data"][0]["token"]
        self.create_meetup(access_token, MEETUP)
        access_token = self.get_access_token(USER_REGISTRATION, USER_LOGIN)
        self.create_question(access_token, QUESTION)
        access_token = self.get_access_token(NEW_USER_REGISTRATION, NEW_USER_LOGIN)
        res = self.client().patch(
            '/api/v2/questions/1/upvote',
            headers=self.get_authentication_headers(access_token)
        )
        res = self.client().patch(
            '/api/v2/questions/1/upvote',
            headers=self.get_authentication_headers(access_token)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 423)
        self.assertEqual(response_msg["message"]["error"], "A user can only vote once")
