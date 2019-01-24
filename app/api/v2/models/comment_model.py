"""This module represents the comments entity"""
from app.api.v2.models.base_model import BaseModel

TABLE_NAME = 'comments'

class CommentsModel(BaseModel):
    """Entity representation for a comment"""
    def __init__(self, **kwargs):
        super().__init__()
        self.comment = kwargs.get('comment')

    def save(self, question_id, user_id):
        """Add a new comment to the data store"""
        query = """INSERT INTO comments(
        question_id, user_id, comment) VALUES(
        (SELECT id FROM questions WHERE id={}),
        (SELECT id FROM users WHERE id={}), '{}')""".format(
            question_id,
            user_id,
            self.comment
        )
        self.cursor.execute(query)
        self.connection.commit()
