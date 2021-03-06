"""This module represents the user view"""
from flask import abort
from flask_jwt_extended import create_access_token
from flask_restful import Resource, reqparse

from flasgger import swag_from

from app.api.v2.utils.validator import ValidationHandler
from app.api.v2.models.user_model import UserModel

class UserRegistration(Resource):
    """Register a new user"""
    @swag_from('docs/auth_register.yml')
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
        parser.add_argument('password', type=str, required=True, help='password cannot be blank!')

        data = parser.parse_args()

        # Create an instance of a user
        user = UserModel(
            firstname=data['firstname'],
            lastname=data['lastname'],
            othername=data['othername'],
            email=data['email'],
            phoneNumber=data['phoneNumber'],
            username=data['username'],
            password=UserModel.generate_password_hash(data['password'])
        )

        username = data['username']
        password = data['password']
        email = data['email']

        # Validate firstname
        ValidationHandler.validate_field_empty('Firstname', data['firstname'])

        # Validate lastname
        ValidationHandler.validate_field_empty('Lastname', data['lastname'])

        # Validate othername
        ValidationHandler.validate_field_empty('Othername', data['othername'])

        # Validate phonenumber
        ValidationHandler.validate_field_empty('PhoneNumber', data['phoneNumber'])
        ValidationHandler.validate_phone_number(data['phoneNumber'])

        # Validate the username
        ValidationHandler.validate_correct_username(username)

        # Validate the email address
        ValidationHandler.validate_email_address(email)

        # Validate the password
        ValidationHandler.validate_password(password)

        if user.find_user_by_username('username', username):
            abort(409, {
                "error": "Username '{}' already taken!".format(username),
                "status": 409
            })

        if user.find_user_by_email('email', email):
            abort(409, {
                "error": "Email address '{}' already in use!".format(email),
                "status": 409
            })

        user.add_user()

        result = user.find_user_by_username('username', username)

        return {
            "status": 201,
            "data": [
                {
                    "user": UserModel.to_json(result),
                    "message": "User account created successfully"
                }
            ]
        }, 201

class UserLogin(Resource):
    """Log in a user"""
    @swag_from('docs/auth_login.yml')
    def post(self):
        """Sign In a registered user"""
        user = UserModel()

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('username', type=str, required=True, help='username cannot be blank!')
        parser.add_argument('password', type=str, required=True, help='password cannot be blank!')

        data = parser.parse_args()

        current_user = user.find_user_by_username('username', data['username'])

        ValidationHandler.validate_correct_username(data['username'])
        ValidationHandler.validate_password(data['password'])

        if not current_user:
            abort(404, {
                "error": "Username and password not found!",
                "status": 404
            })
        if UserModel.verify_password_hash(data['password'], current_user['password']):
            access_token = create_access_token(identity=data['username'])
            return {
                "status": 200,
                "data": [
                    {
                        "token": access_token,
                        "user": UserModel.to_json(current_user),
                        "message": "Logged in as '{}'".format(current_user['username'])
                    }
                ]
            }, 200
        abort(401, {
            "error": "Username and password not found!",
            "status": 401
        })
        return None
