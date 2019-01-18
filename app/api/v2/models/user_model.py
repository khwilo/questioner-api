"""Module representing a user entity"""
from datetime import datetime

from app.api.v2.database.database_config import initiate_db

class UserModel:
    """Entity representation for a user"""
    def __init__(self, **kwargs):
        self.firstname = kwargs.get('firstname')
        self.lastname = kwargs.get('lastname')
        self.othername = kwargs.get('othername')
        self.email = kwargs.get('email')
        self.phone_number = kwargs.get('phone_number')
        self.username = kwargs.get('username')
        self.registered = str(datetime.utcnow())
        self.is_admin = kwargs.get('is_admin')
        self.password = kwargs.get('password')

    def add_user(self):
        """Add a new user to the 'users' table"""
        database = initiate_db()
        db_cursor = database.cursor()
        query = """INSERT INTO users(
        firstname, lastname, othername, email, phone_number, username, is_admin, password) VALUES(
        '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');""".format(
            self.firstname,
            self.lastname,
            self.othername,
            self.email,
            self.phone_number,
            self.username,
            self.is_admin,
            self.password)
        db_cursor.execute(query)
        database.commit()
        db_cursor.close()
