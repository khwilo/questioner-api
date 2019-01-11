'''This module represents the question entity'''
from datetime import datetime

from app.api.v1.utils.serializer import serialize
from app.api.v1.models.meetup_model import MeetupModel

QUESTIONS = [] # Data store for the questions

class QuestionModel:
    '''Entity representation for a question'''
    def __init__(self, created_by, meetup, title, body):
        self.question_id = len(QUESTIONS) + 1
        self.created_on = str(datetime.utcnow())
        self.created_by = created_by
        self.meetup = meetup
        self.title = title
        self.body = body
        self.votes = 0

    @staticmethod
    def add_question(question, meetup_id):
        '''Add a new question to the data store'''
        QUESTIONS.append(question)
        meetup = MeetupModel.get_meetup_by_id(int(meetup_id))
        meetup["questions"].append(serialize(question))
