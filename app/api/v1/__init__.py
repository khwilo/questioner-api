'''
Modularize the app using BluePrints and the API resource
'''
from flask import Blueprint
from flask_restful import Api

from app.api.v1.views.user_view import UserRegistration, UserLogin

AUTH_BLUEPRINT = Blueprint("auth", __name__, url_prefix='/auth')

AUTH_API = Api(AUTH_BLUEPRINT)

AUTH_API.add_resource(UserRegistration, '/register')
AUTH_API.add_resource(UserLogin, '/login')
