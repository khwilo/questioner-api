'''This module represents a user entity'''
from datetime import datetime
from passlib.hash import pbkdf2_sha256 as sha256

from app.api.v2.models.base_model import BaseModel

TABLE_NAME = 'users'

class UserModel(BaseModel):
    '''Entity representation for a user'''
    def __init__(self, **kwargs):
        super().__init__()
        self.firstname = kwargs.get('firstname')
        self.lastname = kwargs.get('lastname')
        self.othername = kwargs.get('othername')
        self.email = kwargs.get('email')
        self.phone_number = kwargs.get('phoneNumber')
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

    @staticmethod
    def generate_password_hash(password):
        '''Generate the hash of the password'''
        return sha256.hash(password)

    @staticmethod
    def verify_password_hash(password, hashed_password):
        '''Compare the password with its hashed value'''
        return sha256.verify(password, hashed_password)

    @staticmethod
    def to_json(result):
        '''Turn the table result to JSON'''
        return {
            'id': result['id'],
            'firstname': result['firstname'],
            'lastname': result['lastname'],
            'othername': result['othername'],
            'email': result['email'],
            'phoneNumber': result['phone_number'],
            'username': result['username'],
            'registered ': str(result['registered']),
            'isAdmin': result['is_admin']
        }
