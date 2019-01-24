"""Module representing the base model"""
from psycopg2.extras import RealDictCursor

from db import establish_connection

class BaseModel:
    """Definitions for the base model"""
    def __init__(self):
        self.connection = establish_connection()
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)

    def find_item_if_exists(self, tablename, column, value):
        """Find an item if it exists"""
        query = """SELECT * FROM {} WHERE {}='{}';""".format(tablename, column, value)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result

    def fetch_all(self, tablename):
        """Fetch all items form a table"""
        query = """SELECT * FROM {};""".format(tablename)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result
