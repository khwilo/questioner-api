'''This module represents the meetup view'''
from flask import abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import reqparse, Resource

from app.api.v2.models.meetup_model import MeetupModel
from app.api.v2.models.user_model import UserModel

class MeetupList(Resource):
    '''Request on a meetup list'''
    @jwt_required
    def post(self):
        '''Create a meetup record'''
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('location', required=True, help="location cannot be blank!")
        parser.add_argument('images')
        parser.add_argument('topic', required=True, help="topic cannot be blank!")
        parser.add_argument('description', required=True, help="description cannot be blank!")
        parser.add_argument('happeningOn', required=True, help="happeningOn cannot be blank!")
        parser.add_argument('tags')
        data = parser.parse_args()

        user = UserModel()
        current_user = get_jwt_identity()
        user = user.find_user_by_username('username', current_user)

        if not user:
            abort(401, {
                "error": "This action required loggin in!",
                "status": 401
            })

        if user['is_admin']:
            meetup = MeetupModel(
                location=data['location'],
                images=data['images'],
                topic=data['topic'],
                description=data['description'],
                happening_on=MeetupModel.convert_string_to_date(data['happeningOn']),
                tags=data['tags']
            )
            meetup.save()
            return {
                'status': 201,
                'message': "Meetup created successfully"
            }, 201
        abort(403, {
            "error": "Only administrators can create a meetup",
            "status": 403
        })
        return None

class Meetup(Resource):
    '''Request on a meetup item'''
    @jwt_required
    def get(self, meetup_id):
        '''Fetch a single meetup item'''
        meetup_obj = MeetupModel()
        if meetup_id.isdigit():
            meetup = meetup_obj.get_meetup_by_id('id', int(meetup_id))
            if not meetup:
                abort(404, {
                    "error": "Meetup with id '{}' doesn't exist!".format(meetup_id),
                    "status": 404
                })
            return {
                'status': 200,
                'data': MeetupModel.to_dict(meetup)
            }, 200
        abort(400, {
            "error": "Meetup ID must be an Integer",
            "status": 400
        })
        return None

class UpcomingMeetup(Resource):
    '''Request on an upcoming meetup item'''
    @jwt_required
    def get(self):
        '''Fetch all upcoming meetups'''
        meetups = MeetupModel.get_all_meetups()
        if meetups == []:
            abort(404, {
                "error": "No meetup is available",
                "status": 404
            })
        return {
            'status': 200,
            'data': sorted(meetups, key=lambda item: item['happening_on'], reverse=True)
        }, 200
