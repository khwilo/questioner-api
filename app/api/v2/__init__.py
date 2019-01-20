'''
Modularize the app using BluePrints
'''
from flask import Blueprint
from flask_restful import Api

from app.api.v2.views.user_view import UserRegistration as registration_v2

API_V2_BLUEPRINT = Blueprint("api_v2", __name__, url_prefix="/api/v2")

API_V2 = Api(API_V2_BLUEPRINT)

API_V2.add_resource(registration_v2, '/register')
