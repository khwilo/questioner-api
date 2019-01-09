'''This module represents the user view'''
from flask_restful import Resource, reqparse

from app.api.v1.utils.serializer import serialize
from app.api.v1.models.user_model import UserModel

class UserRegistration(Resource):
    """Register a new user"""
    def post(self):
        """Create a user account"""
        parser = reqparse.RequestParser()
        parser.add_argument('firstname', type=str, required=True, help='firstname cannot be blank!')
        parser.add_argument('lastname', type=str, required=True, help='lastname cannot be blank!')
        parser.add_argument('othername', type=str, required=True, help='othername cannot be blank!')
        parser.add_argument('email', type=str, required=True, help='email cannot be blank!')
        parser.add_argument('phone_number', type=str, required=True, help='phone_number cannot be blank!')
        parser.add_argument('username', type=str, required=True, help='username cannot be blank!')
        parser.add_argument('is_admin', type=bool, required=True, help='is_admin cannot be blank!')
        parser.add_argument('password', type=str, required=True, help='password cannot be blank!')

        data = parser.parse_args()

        # Create an instance of a user
        user = UserModel(
            firstname=data['firstname'],
            lastname=data['lastname'],
            othername=data['othername'],
            email=data['email'],
            phone_number=data['phone_number'],
            username=data['username'],
            is_admin=data['is_admin'],
            password=data['password']
        )

        username = data['username']
        password = data['password']

        # Validate the username
        if username.isdigit():
            return {
                'message': 'username cannot consist of digits only'
            }, 400
        if not username or not username.split():
            return {
                'message': 'username cannot be empty'
            }, 400

        # Validate the password
        if not password or not password.split():
            return {
                'message': 'password cannot be empty'
            }, 400

        UserModel.add_user(serialize(user))

        return {
            "status": 201,
            "data": [
                {
                    "message": "Create a user record"
                }
            ]
        }, 201
