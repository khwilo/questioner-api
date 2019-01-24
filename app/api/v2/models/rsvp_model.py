"""This module represents an meetup rsvp entity"""

from app.api.v2.models.base_model import BaseModel

class RsvpModel(BaseModel):
    """Entity representation for an RSVP"""
    def __init__(self, **kwargs):
        super().__init__()
        self.response = kwargs.get('response')

    def save(self, meetup_id, user_id):
        """Save a meetup RSVP"""
        query = """INSERT INTO rsvps(
        meetup_id, user_id, response) VALUES(
        (SELECT id FROM meetups WHERE id={}),
        (SELECT id FROM users WHERE id={}), '{}')""".format(
            meetup_id,
            user_id,
            self.response
        )
        self.cursor.execute(query)
        self.connection.commit()
