'''
Modularize the app using BluePrints and the API resource
'''
from flask import Blueprint
from flask_restful import Api

from app.api.v1.views.meetup_view import MeetupList
from app.api.v1.views.user_view import UserRegistration, UserLogin

AUTH_BLUEPRINT = Blueprint("auth", __name__, url_prefix='/auth')
API_BLUEPRINT = Blueprint("api", __name__, url_prefix='/api/v1')

AUTH = Api(AUTH_BLUEPRINT)
API = Api(API_BLUEPRINT)

AUTH.add_resource(UserRegistration, '/register')
AUTH.add_resource(UserLogin, '/login')

API.add_resource(MeetupList, '/meetups')
