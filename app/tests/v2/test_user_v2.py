'''This module represents tests for the user entity'''
import json

from app.tests.v2.test_base_v2 import BaseTestDbTestCase

class UsersDbTestCase(BaseTestDbTestCase):
    '''Test definitions for a user'''
    def test_db_user_registration(self):
        '''Test a user account can be created in the database'''
        res = self.client().post(
            '/api/v2/register',
            headers=self.get_accept_content_type_headers(),
            data=json.dumps(self.user_registration)
        )
        self.assertEqual(res.status_code, 201)
