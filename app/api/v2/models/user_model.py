'''This module represents a user entity'''
from datetime import datetime
from passlib.hash import pbkdf2_sha256 as sha256

from app.api.v2.utils.utility import Utility

USERS = [] # Data store for the users

class UserModel:
    '''Entity representation for a user'''
    def __init__(self, **kwargs):
        self.user_id = len(USERS) + 1
        self.firstname = kwargs.get('firstname')
        self.lastname = kwargs.get('lastname')
        self.othername = kwargs.get('othername')
        self.email = kwargs.get('email')
        self.phone_number = kwargs.get('phone_number')
        self.username = kwargs.get('username')
        self.registered = str(datetime.utcnow())
        self.is_admin = kwargs.get('is_admin')
        self.password = kwargs.get('password')

    def get_user_id(self):
        '''Fetch a user id'''
        return self.user_id

    @staticmethod
    def generate_password_hash(password):
        '''Generate the hash of the password'''
        return sha256.hash(password)

    @staticmethod
    def verify_password_hash(password, hashed_password):
        '''Compare the password with its hashed value'''
        return sha256.verify(password, hashed_password)

    @staticmethod
    def add_user(user):
        '''Add a new user to the data store'''
        USERS.append(user)

    @staticmethod
    def get_all_users():
        '''Fetch all users'''
        return USERS

    @staticmethod
    def get_user_by_username(username):
        '''Fetch a user given a username'''
        return Utility.fetch_item(username, 'username', USERS)
