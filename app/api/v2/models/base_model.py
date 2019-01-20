'''Module representing the base model'''
from flask import g
from psycopg2.extras import RealDictCursor

from db import establish_connection

class BaseModel:
    '''Definitions for the base model'''
    def __init__(self):
        self.connection = BaseModel.check_connection()
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)

    @classmethod
    def check_connection(cls):
        '''Check if the database connection exists'''
        if 'connection' not in g:
            connection = establish_connection()
        return connection

    def find_item_if_exists(self, tablename, column, value):
        """Find an item if it exists"""
        query = """SELECT * FROM {} WHERE {}='{}';""".format(tablename, column, value)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result
