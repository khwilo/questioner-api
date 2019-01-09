'''This module represents a user entity'''
from datetime import datetime
from passlib.hash import pbkdf2_sha256 as sha256

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
        user = {}
        for index, _ in enumerate(USERS):
            if USERS[index].get('username') == username:
                user = USERS[index]
        return user
