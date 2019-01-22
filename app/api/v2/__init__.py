'''
Modularize the app using BluePrints and the API resource
'''
from flask import Blueprint
from flask_restful import Api

from app.api.v2.views.meetup_view import MeetupList, Meetup, UpcomingMeetup
from app.api.v2.views.question_view import Question, Upvote, Downvote
from app.api.v2.views.rsvp_view import Rsvp
from app.api.v2.views.user_view import UserRegistration, UserLogin

AUTH_BLUEPRINT = Blueprint("auth", __name__, url_prefix='/api/v2/auth')
API_BLUEPRINT = Blueprint("api", __name__, url_prefix='/api/v2')

AUTH = Api(AUTH_BLUEPRINT)
API = Api(API_BLUEPRINT)

AUTH.add_resource(UserRegistration, '/signup')
AUTH.add_resource(UserLogin, '/login')

API.add_resource(MeetupList, '/meetups')
API.add_resource(Meetup, '/meetups/<meetup_id>')
API.add_resource(UpcomingMeetup, '/meetups/upcoming/')
API.add_resource(Question, '/meetups/<meetup_id>/questions')
API.add_resource(Upvote, '/meetups/<meetup_id>/questions/<question_id>/upvote')
API.add_resource(Downvote, '/meetups/<meetup_id>/questions/<question_id>/downvote')
API.add_resource(Rsvp, '/meetups/<meetup_id>/rsvps')
