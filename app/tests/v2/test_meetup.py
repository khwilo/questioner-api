'''This module represents tests for the meetup entity'''
import json

from app.api.v2.models.meetup_model import MEETUPS
from app.tests.v2.test_base import BaseTestCase

class MeetupTestCase(BaseTestCase):
    '''Test definitions for a meetup'''
    def test_admin_create_meetup(self):
        '''Test an administrator can create a meetup'''
        pass

    def test_user_cannot_create_meetup(self):
        '''Test a regular user cannot create a meetup'''
        pass

    def test_fetch_one_meetup(self):
        '''Test the API can fetch one meetup'''
        pass

    def test_fetch_incorrect_meetup_id(self):
        '''Test the API cannot fetch a meetup with an incorrect ID'''
        pass

    def test_empty_meetup_item(self):
        '''Test the API cannot read data from an empty meetup item'''
        pass

    def test_fetch_all_meetups(self):
        '''Test the API can fetch all meetups'''
        pass

    def test_fetch_empty_meetup_list(self):
        '''Test the API cannot fetch data from an empty meetup list data store'''
        pass
