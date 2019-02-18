"""This module represents a meetup entity"""
from datetime import datetime

from app.api.v2.models.base_model import BaseModel

TABLE_NAME = 'meetups'

class MeetupModel(BaseModel):
    """Entity representation for a meetup"""
    def __init__(self, **kwargs):
        super().__init__()
        self.location = kwargs.get('location')
        self.images = kwargs.get('images')
        self.topic = kwargs.get('topic')
        self.description = kwargs.get('description')
        self.happening_on = kwargs.get('happening_on')
        self.tags = kwargs.get('tags')

    def save(self):
        """Add a new meetup to the data store"""
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

    def get_meetup_by_id(self, meetup_id, value):
        """Return a meetup given a meetup id"""
        result = self.find_item_if_exists(TABLE_NAME, meetup_id, value)
        return result

    def get_all_meetups(self):
        """Fetch all meetups"""
        result = self.fetch_all(TABLE_NAME)
        return result

    def delete_meetup_by_id(self, meetup_id, value):
        """Delete a meetup given its ID"""
        self.delete_one(TABLE_NAME, meetup_id, value)

    def find_meetup_by_location_and_happening_time(self, location, happening_on):
        """Find a meetup by location and the happening time"""
        result = self.find_item_by_two_columns(
            tablename=TABLE_NAME,
            column1='m_location',
            value1=location,
            column2='happening_on ',
            value2=happening_on
        )
        return result

    @staticmethod
    def convert_string_to_date(string_date):
        """Convert string object to datetime object"""
        return str(datetime.strptime(string_date, '%b %d %Y, %I:%M %p'))

    @staticmethod
    def to_dict(result):
        """Convert meetup model to dictionary"""
        return {
            'id': result['id'],
            'createdOn': str(result['created_on']),
            'location': result['m_location'],
            'images': result['images'],
            'topic': result['topic'],
            'description': result['m_description'],
            'happeningOn': str(result['happening_on']),
            'tags': result['tags']
        }
