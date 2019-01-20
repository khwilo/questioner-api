"""Module representing a user entity"""
from datetime import datetime

from app.api.v2.models.base_model import BaseModel

TABLE_NAME = 'users'

class UserModel(BaseModel):
    """Entity representation for a user"""
    def __init__(self, **kwargs):
        super().__init__()
        self.firstname = kwargs.get('firstname')
        self.lastname = kwargs.get('lastname')
        self.othername = kwargs.get('othername')
        self.email = kwargs.get('email')
        self.phone_number = kwargs.get('phone_number')
        self.username = kwargs.get('username')
        self.registered = str(datetime.utcnow())
        self.password = kwargs.get('password')

    def add_user(self):
        """Add a new user to the 'users' table"""
        query = """INSERT INTO users(
        firstname, lastname, othername, email, phone_number, username, password) VALUES(
        '{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(
            self.firstname,
            self.lastname,
            self.othername,
            self.email,
            self.phone_number,
            self.username,
            self.password)
        self.cursor.execute(query)
        self.connection.commit()

    def find_user_by_username(self, username, value):
        """Find a user by username"""
        result = self.find_item_if_exists(TABLE_NAME, username, value)
        return result

    def find_user_by_email(self, email, value):
        """Find a user by email address"""
        result = self.find_item_if_exists(TABLE_NAME, email, value)
        return result

    def user_to_dict(self):
        '''Turn user object to dictionary'''
        return {
            'firstname': self.firstname,
            'lastname': self.lastname,
            'othername': self.othername,
            'email': self.email,
            'phone_number': self.phone_number,
            'username': self.username,
            'registered': self.registered,
            'password': self.password
        }
