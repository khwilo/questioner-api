"""This module represent tests for the comments entity"""
import json

from app.tests.v2.sample_data import USER_REGISTRATION, USER_LOGIN, COMMENT, \
ADMIN_LOGIN, MEETUP, NEW_USER_REGISTRATION, NEW_USER_LOGIN, QUESTION
from app.tests.v2.test_base import BaseTestCase

class CommentTestCase(BaseTestCase):
    """Test definitions for a comment"""
    def test_comment_on_question(self):
        """Test that a user can comment on a question"""
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
        res = self.client().post(
            '/api/v2/questions/1/comments',
            headers=self.get_authentication_headers(access_token),
            data=json.dumps(COMMENT)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 201)
        self.assertEqual(response_msg["message"], "Comment posted successfully!")


    def test_comment_to_non_existing_question(self):
        """Test that a comment cannot be created for a non-existing question"""
        access_token = self.get_access_token(USER_REGISTRATION, USER_LOGIN)
        res = self.client().post(
            '/api/v2/questions/2/comments',
            headers=self.get_authentication_headers(access_token),
            data=json.dumps(COMMENT)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 404)
        self.assertEqual(response_msg["message"]["error"], "Question with id '2' doesn't exist!")

    def test_incorrect_question_id(self):
        """Test an incorrect question ID is validated"""
        access_token = self.get_access_token(USER_REGISTRATION, USER_LOGIN)
        res = self.client().post(
            '/api/v2/questions/i/comments',
            headers=self.get_authentication_headers(access_token),
            data=json.dumps(COMMENT)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 400)
        self.assertEqual(response_msg["message"]["error"], "Question ID must be an integer value")
