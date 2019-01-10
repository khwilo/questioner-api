'''This module represents a meetup entity'''
from datetime import datetime

from app.api.v1.utils.utility import fetch_item

MEETUPS = [] # Data store for the meetups

class MeetupModel:
    '''Entity representation for a meetup'''
    def __init__(self, location, topic, happening_on, tags, images=None):
        self.meetup_id = len(MEETUPS) + 1
        self.created_on = str(datetime.utcnow())
        self.location = location
        self.images = "" if images is None else images
        self.topic = topic
        self.happening_on = happening_on
        self.tags = tags

    def get_meetup_id(self):
        '''Fetch the meetup id'''
        return self.get_meetup_id

    @staticmethod
    def convert_string_to_date(string_date):
        '''Convert string object to datetime object'''
        return str(datetime.strptime(string_date, '%b %d %Y %I:%M%p'))

    @staticmethod
    def add_meetup(meetup):
        '''Add a new meetup to the data store'''
        MEETUPS.append(meetup)

    @staticmethod
    def get_meetup_by_id(meetup_id):
        '''Return a meetup given a meetup id'''
        return fetch_item(meetup_id, 'meetup_id', MEETUPS)

    @staticmethod
    def get_all_meetups():
        '''Fetch all meetups'''
        return MEETUPS
