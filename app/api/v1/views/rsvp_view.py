'''This module represents the rsvp view'''
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import reqparse, Resource

from app.api.v1.utils.serializer import serialize
from app.api.v1.models.rsvp_model import RsvpModel
from app.api.v1.models.user_model import UserModel
from app.api.v1.models.meetup_model import MeetupModel

class Rsvp(Resource):
    '''Request on a meetup RSVP'''
    @jwt_required
    def post(self, meetup_id):
        '''Respond to a meetup RSVP'''
        parser = reqparse.RequestParser()
        parser.add_argument('response', required=True, help='response is required!')
        data = parser.parse_args()

        current_user = get_jwt_identity()
        user = UserModel.get_user_by_username(current_user)

        meetup = MeetupModel.get_meetup_by_id(int(meetup_id))

        rsvp = RsvpModel(
            meetup=int(meetup_id),
            user=user['user_id'],
            response=data['response']
        )

        RsvpModel.add_rsvp(serialize(rsvp))

        return {
            'status': 201,
            'data': [
                {
                    "meetup": int(meetup_id),
                    "topic": meetup["topic"],
                    "status": data['response']
                }
            ]
        }, 201
