'''This module represents the meetup view'''
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import reqparse, Resource

from app.api.v1.utils.serializer import serialize
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
        parser.add_argument('happening_on', required=True, help="location cannot be blank!")
        parser.add_argument('tags', action='append')
        data = parser.parse_args()

        current_user = get_jwt_identity()
        user = UserModel.get_user_by_username(current_user)

        if not user:
            return {
                'message': "This action required loggin in!"
            }, 401

        if user['is_admin']:
            meetup = MeetupModel(
                location=data['location'],
                images=data['images'],
                topic=data['topic'],
                happening_on=MeetupModel.convert_string_to_date(data['happening_on']),
                tags=data['tags']
            )
            MeetupModel.add_meetup(serialize(meetup))
            return {
                'status': 201,
                'data': [serialize(meetup)]
            }, 201
        return {
            'message': "Only administrators can create a meetup"
        }, 401

class Meetup(Resource):
    '''Request on a meetup item'''
    @jwt_required
    def get(self, meetup_id):
        '''Fetch a single meetup item'''
        if meetup_id.isdigit():
            meetup = MeetupModel.get_meetup_by_id(int(meetup_id))
            if meetup == {}:
                return {
                    'message': "Meetup with id '{}' doesn't exist!".format(meetup_id)
                }, 404
            return {
                'status': 200,
                'data': [meetup]
            }, 200
        return {
            'message': 'Meetup ID must be an Integer'
        }, 400

class UpcomingMeetup(Resource):
    '''Request on an upcoming meetup item'''
    @jwt_required
    def get(self):
        '''Fetch all upcoming meetups'''
        meetups = MeetupModel.get_all_meetups()
        if meetups == []:
            return {
                'message': 'No meetup is available'
            }, 404
        return {
            'status': 200,
            'data': sorted(meetups, key=lambda item: item['happening_on'], reverse=True)
        }, 200
