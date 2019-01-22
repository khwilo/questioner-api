'''This module represents the meetup view'''
from flask import abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import reqparse, Resource

from app.api.v1.utils.utility import Utility
from app.api.v1.models.meetup_model import MeetupModel
from app.api.v1.models.user_model import UserModel

class MeetupList(Resource):
    '''Request on a meetup list'''
    @jwt_required
    def post(self):
        '''Create a meetup record'''
        parser = reqparse.RequestParser()
        parser.add_argument('location', required=True, help="location cannot be blank!")
        parser.add_argument('images', action='append')
        parser.add_argument('topic', required=True, help="location cannot be blank!")
        parser.add_argument('happeningOn', required=True, help="location cannot be blank!")
        parser.add_argument('tags', action='append')
        data = parser.parse_args()

        current_user = get_jwt_identity()
        user = UserModel.get_user_by_username(current_user)

        if not user:
            abort(401, 'This action required loggin in!')

        if user['is_admin']:
            meetup = MeetupModel(
                location=data['location'],
                images=data['images'],
                topic=data['topic'],
                happening_on=MeetupModel.convert_string_to_date(data['happeningOn']),
                tags=data['tags']
            )
            MeetupModel.add_meetup(Utility.serialize(meetup))
            return {
                'status': 201,
                'data': [Utility.serialize(meetup)]
            }, 201
        abort(403, "Only administrators can create a meetup")
        return None

class Meetup(Resource):
    '''Request on a meetup item'''
    @jwt_required
    def get(self, meetup_id):
        '''Fetch a single meetup item'''
        if meetup_id.isdigit():
            meetup = MeetupModel.get_meetup_by_id(int(meetup_id))
            if meetup == {}:
                abort(404, "Meetup with id '{}' doesn't exist!".format(meetup_id))
            return {
                'status': 200,
                'data': [meetup]
            }, 200
        abort(400, 'Meetup ID must be an Integer')
        return None

class UpcomingMeetup(Resource):
    '''Request on an upcoming meetup item'''
    @jwt_required
    def get(self):
        '''Fetch all upcoming meetups'''
        meetups = MeetupModel.get_all_meetups()
        if meetups == []:
            abort(404, 'No meetup is available')
        return {
            'status': 200,
            'data': sorted(meetups, key=lambda item: item['happening_on'], reverse=True)
        }, 200
