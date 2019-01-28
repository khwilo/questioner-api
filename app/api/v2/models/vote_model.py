"""This module represents the vote entity"""
from app.api.v2.models.base_model import BaseModel

TABLE_NAME = 'votes'

class VoteModel(BaseModel):
    """Entity representation for a vote"""
    def save(self, question_id, user_id):
        """Save a user vote"""
        query = """INSERT INTO votes(
        question_id, user_id) VALUES(
        (SELECT id FROM questions WHERE id={}),
        (SELECT id FROM users WHERE id={}))""".format(
            question_id,
            user_id
        )
        self.cursor.execute(query)
        self.connection.commit()

    def get_vote(self, q_value, u_value):
        """Fetch a vote by question_id and user_id"""
        result = self.find_item_by_two_columns(
            tablename=TABLE_NAME,
            column1='question_id',
            value1=q_value,
            column2='user_id',
            value2=u_value
        )
        return result
