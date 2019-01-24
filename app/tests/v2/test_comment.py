"""This module represent tests for the comments entity"""
import json

from app.tests.v2.sample_data import ADMIN_LOGIN, USER_REGISTRATION, \
USER_LOGIN, MEETUP, QUESTION, COMMENT
from app.tests.v2.test_base import BaseTestCase

class CommentTestCase(BaseTestCase):
    """Test definitions for a comment"""
    def test_comment_to_non_existing_question(self):
        """Test that  a comment cannot be created for a non-existing question"""
        access_token = self.get_access_token(USER_REGISTRATION, USER_LOGIN)
        res = self.client().post(
            '/api/v2/questions/2/comments',
            headers=self.get_authentication_headers(access_token),
            data=json.dumps(COMMENT)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 404)
        self.assertEqual(response_msg["message"]["error"], "Question with id '2' doesn't exist!")

    def test_comment_with_incorrect_id(self):
        """Test a wrong comment ID is validated"""
        access_token = self.get_access_token(USER_REGISTRATION, USER_LOGIN)
        res = self.client().post(
            '/api/v2/questions/i/comments',
            headers=self.get_authentication_headers(access_token),
            data=json.dumps(COMMENT)
        )
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res.status_code, 400)
        self.assertEqual(response_msg["message"]["error"], "Question ID must be an integer value")
