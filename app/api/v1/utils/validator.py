'''Module for handling validations'''
from flask import abort

class ValidationHandler:
    '''Methods to validate the data provided by the API'''
    @staticmethod
    def validate_correct_username(username):
        '''Validation for a name'''
        if username.isdigit():
            abort(400, 'username cannot consist of digits only')
        if not username or not username.split():
            abort(400, 'username cannot be empty')

    @staticmethod
    def validate_existing_user(users, username):
        '''Validation for an existing user'''
        if next(filter(lambda u: u['username'] == username, users), None):
            abort(409, "A user with username '{}' already exists!".format(username))

    @staticmethod
    def validate_password(password):
        '''Validation for a password'''
        if not password or not password.split():
            abort(400, "password cannot be empty")
