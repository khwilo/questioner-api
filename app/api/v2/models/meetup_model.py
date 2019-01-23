'''This module represents a meetup entity'''
from datetime import datetime

from app.api.v2.models.base_model import BaseModel
from app.api.v2.utils.utility import Utility

TABLE_NAME = 'meetups'

class MeetupModel(BaseModel):
    '''Entity representation for a meetup'''
    def __init__(self, **kwargs):
        super().__init__()
        self.location = kwargs.get('location')
        self.images = kwargs.get('images')
        self.topic = kwargs.get('topic')
        self.description = kwargs.get('description')
        self.happening_on = kwargs.get('happening_on')
        self.tags = kwargs.get('tags')

    def save(self):
        '''Add a new meetup to the data store'''
        query = """INSERT INTO meetups(
        m_location, images, topic, m_description, happening_on, tags) VALUES(
        '{}', '{}', '{}', '{}', '{}', '{}')""".format(
            self.location,
            self.images,
            self.topic,
            self.description,
            self.happening_on,
            self.tags
        )
        self.cursor.execute(query)
        self.connection.commit()

    @staticmethod
    def convert_string_to_date(string_date):
        '''Convert string object to datetime object'''
        return str(datetime.strptime(string_date, '%b %d %Y %I:%M%p'))

    @staticmethod
    def get_meetup_by_id(meetup_id):
        '''Return a meetup given a meetup id'''
        pass

    @staticmethod
    def get_all_meetups():
        '''Fetch all meetups'''
        pass

    @staticmethod
    def get_question_by_id(meetup, question_id):
        '''Return a question to a meetup by its ID'''
        pass
