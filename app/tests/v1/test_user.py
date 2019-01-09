'''This module represents tests for the user entity'''
import json

from app.tests.v1.test_base import BaseTestCase

class UserTestCase(BaseTestCase):
    '''Test definitions for a user'''
    def test_user_registration(self):
        '''Test the API can register a user'''
        res = self.client().post(
            '/auth/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(self.user_registration)
        )
        self.assertEqual(res.status_code, 201)
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(response_msg["status"], 201)
        self.assertTrue(response_msg["data"][0]["message"])
        self.assertEqual(response_msg["data"][0]["message"], "Create a user record")