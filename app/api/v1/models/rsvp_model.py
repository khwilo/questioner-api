'''This module represents an meetup rsvp entity'''

RSVPS = [] # Data store for the RSVP

class RsvpModel:
    '''Entity representation for an RSVP'''
    def __init__(self, meetup, user, response):
        self.rsvp_id = len(RSVPS) + 1
        self.meetup = meetup
        self.user = user
        self.response = response

    @staticmethod
    def add_rsvp(rsvp):
        '''Add an RSVP to the data store'''
        RSVPS.append(rsvp)
