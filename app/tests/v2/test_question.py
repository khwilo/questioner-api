'''This module represents tests for the question entity'''
import json

from app.api.v2.models.meetup_model import MEETUPS
from app.tests.v2.test_base import BaseTestCase

class QuestionTestCase(BaseTestCase):
    '''Test definitions for a question'''
    def test_create_question(self):
        '''Test the API can create a question'''
        pass

    def test_ask_non_existent_meetup(self):
        '''Test the API cannot post a question to a non-existent meetup'''
        pass

    def test_upvote_question(self):
        '''Test the API can upvote a question'''
        pass

    def test_downvote_question(self):
        '''Test the API can downvote a question'''
        pass
