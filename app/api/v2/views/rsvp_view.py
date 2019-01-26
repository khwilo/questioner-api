"""This module represents the rsvp view"""
from flask import abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import reqparse, Resource

from flasgger import swag_from

from app.api.v2.models.rsvp_model import RsvpModel
from app.api.v2.models.user_model import UserModel
from app.api.v2.models.meetup_model import MeetupModel

class Rsvp(Resource):
    """Request on a meetup RSVP"""
    @jwt_required
    @swag_from('docs/rsvp_meetup.yml')
    def post(self, meetup_id):
        """Respond to a meetup RSVP"""
        parser = reqparse.RequestParser()
        parser.add_argument('response', required=True, help='response is required!')
        data = parser.parse_args()

        if meetup_id.isdigit():
            user_obj = UserModel()
            meetup_obj = MeetupModel()
            current_user = get_jwt_identity()
            user = user_obj.find_user_by_username('username', current_user)
            meetup = meetup_obj.get_meetup_by_id('id', int(meetup_id))

            if not meetup:
                abort(404, {
                    "error": "Meetup with id '{}' doesn't exist!".format(meetup_id),
                    "status": 404
                })
            rsvp = RsvpModel(
                response=data['response']
            )
            rsvp.save(int(meetup_id), user['id'])
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
        abort(400, {
            "error": "Meetup ID must be an integer value",
            "status": 400
        })
