'''This module represents the user view'''
from flask import abort
from flask_jwt_extended import create_access_token
from flask_restful import Resource, reqparse

from app.api.v1.utils.utility import Utility
from app.api.v1.utils.validator import ValidationHandler
from app.api.v1.models.user_model import UserModel

class UserRegistration(Resource):
    """Register a new user"""
    def post(self):
        """Create a user account"""
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('firstname', type=str, required=True, help='firstname cannot be blank!')
        parser.add_argument('lastname', type=str, required=True, help='lastname cannot be blank!')
        parser.add_argument('othername', type=str, required=True, help='othername cannot be blank!')
        parser.add_argument('email', type=str, required=True, help='email cannot be blank!')
        parser.add_argument(
            'phoneNumber', type=str, required=True, help='phoneNumber cannot be blank!'
        )
        parser.add_argument('username', type=str, required=True, help='username cannot be blank!')
        parser.add_argument('isAdmin', type=bool, required=True, help='isAdmin cannot be blank!')
        parser.add_argument('password', type=str, required=True, help='password cannot be blank!')

        data = parser.parse_args()

        # Create an instance of a user
        user = UserModel(
            firstname=data['firstname'],
            lastname=data['lastname'],
            othername=data['othername'],
            email=data['email'],
            phone_number=data['phoneNumber'],
            username=data['username'],
            is_admin=data['isAdmin'],
            password=UserModel.generate_password_hash(data['password'])
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

        users = UserModel.get_all_users()

        ValidationHandler.validate_existing_user(users, username)

        UserModel.add_user(Utility.serialize(user))

        return {
            "status": 201,
            "data": [
                {
                    "id": user.get_user_id(),
                    "message": "Create a user record"
                }
            ]
        }, 201

class UserLogin(Resource):
    '''Log in a user'''
    def post(self):
        '''Sign In a registered user'''
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('username', type=str, required=True, help='username cannot be blank!')
        parser.add_argument('password', type=str, required=True, help='password cannot be blank!')

        data = parser.parse_args()

        current_user = UserModel.get_user_by_username(data['username'])

        ValidationHandler.validate_correct_username(data['username'])
        if not current_user:
            abort(404, {
                "error": "User with username '{}' doesn't exist!".format(data['username']),
                "status": 404}
            )

        if UserModel.verify_password_hash(data['password'], current_user['password']):
            access_token = create_access_token(identity=data['username'])
            return {
                'message': "Logged in as '{}'".format(current_user['username']),
                'access_token': access_token
            }, 200
        abort(401, {
            "error": "The password you entered doesn't match",
            "status": 401
        })
        return None
