'''This module represents a meetup entity'''
from datetime import datetime
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
    def add_meetup(meetup):
        '''Add a new meetup to the data store'''
        MEETUPS.append(meetup)

    @staticmethod
    def get_meetup_by_id(meetup_id):
        '''Return a meetup given a meetup id'''
        meetup = {}
        for index, _ in enumerate(MEETUPS):
            if MEETUPS[index].get('meetup_id') == meetup_id:
                meetup = MEETUPS[index]
        return meetup