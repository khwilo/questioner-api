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

    def find_item_by_two_columns(self, **kwargs):
        """Find an item by specifying a combination of two columns"""
        query = """SELECT * FROM {} WHERE {}='{}' AND {}='{}';""".format(
            kwargs.get('tablename'),
            kwargs.get('column1'),
            kwargs.get('value1'),
            kwargs.get('column2'),
            kwargs.get('value2')
        )
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result

    def delete_one(self, tablename, column, value):
        """Delete one record from the database table"""
        query = """DELETE FROM {} WHERE {}={}""".format(tablename, column, value)
        self.cursor.execute(query)
        self.connection.commit()
