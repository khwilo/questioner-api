'''This module represents a user entity'''
from datetime import datetime

USERS = [] # Data store for the users

class UserModel:
    '''Entity representation for a user'''
    def __init__(self, firstname, lastname, othername, email, phone_number, \
                username, is_admin, password):
        self.user_id = len(USERS) + 1
        self.firstname = firstname
        self.lastname = lastname
        self.othername = othername
        self.email = email
        self.phone_number = phone_number
        self.username = username
        self.registered = str(datetime.utcnow())
        self.is_admin = is_admin
        self.password = password

    def get_user_id(self):
        '''Fetch a user id'''
        return self.user_id

    @staticmethod
    def add_user(user):
        '''Add a new user to the data store'''
        USERS.append(user)
