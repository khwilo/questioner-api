'''This module represents the user view'''
from flask import abort
from flask_jwt_extended import create_access_token
from flask_restful import Resource, reqparse

from app.api.v1.utils.validator import ValidationHandler
from app.api.v1.models.user_model import UserModel as UserModel_v1
from app.api.v2.models.user_model import UserModel as UserModel_v2

class UserRegistration(Resource):
    """Register a new user"""
    def post(self):
        """Create a user account"""
        parser = reqparse.RequestParser()
        parser.add_argument('firstname', type=str, required=True, help='firstname cannot be blank!')
        parser.add_argument('lastname', type=str, required=True, help='lastname cannot be blank!')
        parser.add_argument('othername', type=str, required=True, help='othername cannot be blank!')
        parser.add_argument('email', type=str, required=True, help='email cannot be blank!')
        parser.add_argument(
            'phone_number', type=str, required=True, help='phone_number cannot be blank!'
        )
        parser.add_argument('username', type=str, required=True, help='username cannot be blank!')
        parser.add_argument('password', type=str, required=True, help='password cannot be blank!')

        data = parser.parse_args()

        user = UserModel_v2(
            firstname=data['firstname'],
            lastname=data['lastname'],
            othername=data['othername'],
            email=data['email'],
            phone_number=data['phone_number'],
            username=data['username'],
            password=UserModel_v1.generate_password_hash(data['password'])
        )

        username = data['username']
        password = data['password']
        email = data['email']

        # Validate the username
        ValidationHandler.validate_correct_username(username)

        # Validate the email address
        ValidationHandler.validate_email_address(email)

        # Validate the password
        ValidationHandler.validate_password(password)

        if user.find_user_by_username('username', username):
            abort(409, "Username '{}' already taken!".format(username))

        if user.find_user_by_email('email', email):
            abort(409, "Email address '{}' already in use!".format(email))

        token = create_access_token(identity=username)

        user.add_user()

        return {
            "status": 201,
            "data": [
                {
                    "token": token,
                    "user": user.user_to_dict(),
                    "message": "User account created successfully"
                }
            ]
        }, 201

class UserLogin(Resource):
    '''Definitions for login in a user'''
    def post(self):
        '''Log in a registered user'''
        user = UserModel_v2()

        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='username cannot be blank!')
        parser.add_argument('password', type=str, required=True, help='password cannot be blank!')
        data = parser.parse_args()

        current_user = user.find_user_by_username('username', data['username'])

        ValidationHandler.validate_correct_username(data['username'])
        ValidationHandler.validate_password(data['password'])
        if not current_user:
            abort(404, "User with username '{}' doesn't exist!".format(data['username']))
        if UserModel_v1.verify_password_hash(data['password'], current_user['password']):
            token = create_access_token(identity=data['username'])
            return {
                "status": 200,
                "data": [{
                    "token": token,
                    "message": "Logged in as '{}'".format(current_user['username'])
                }]
            }
        abort(401, 'Wrong credentials')
        return None
