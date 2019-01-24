"""This module represents the question entity"""
from app.api.v2.models.base_model import BaseModel

TABLE_NAME = 'questions'

class QuestionModel(BaseModel):
    """Entity representation for a question"""
    def __init__(self, **kwargs):
        super().__init__()
        self.title = kwargs.get('title')
        self.body = kwargs.get('body')

    def save(self, user_id, meetup_id):
        """Add a new question to the datastore"""
        query = """INSERT INTO questions(
        created_by, meetup_id, title, body) VALUES(
        (SELECT id FROM users WHERE id={}),
        (SELECT id FROM meetups WHERE id={}), '{}', '{}')""".format(
            user_id,
            meetup_id,
            self.title,
            self.body
        )
        self.cursor.execute(query)
        self.connection.commit()
