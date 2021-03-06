"""This module represents the meetup view"""
from flask import abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import reqparse, Resource

from flasgger import swag_from

from app.api.v2.models.meetup_model import MeetupModel
from app.api.v2.models.user_model import UserModel

class MeetupList(Resource):
    """Request on a meetup list"""
    @jwt_required
    @swag_from('docs/meetup_post.yml')
    def post(self):
        """Create a meetup record"""
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
        try:
            meetup_time = MeetupModel.convert_string_to_date(data['happeningOn'])
        except ValueError:
            abort(400, {
                "error": "Meetup time doesn't match the format 'Mon DD YYYY, HH:MI AM/PM'"
            })
        venue = data['location']
        if user['is_admin']:
            meetup = MeetupModel(
                location=venue,
                images=data['images'],
                topic=data['topic'],
                description=data['description'],
                happening_on=meetup_time,
                tags=data['tags']
            )
            if not meetup.find_meetup_by_location_and_happening_time(venue, meetup_time):
                meetup.save()
                return {
                    'status': 201,
                    'message': "Meetup created successfully"
                }, 201
            abort(409, {
                "error": "Meetup with the same location and time already exists!",
                "status": 409
            })
        abort(403, {
            "error": "Only administrators can create a meetup",
            "status": 403
        })
        return None

class Meetup(Resource):
    """Request on a meetup item"""
    @jwt_required
    @swag_from('docs/meetup_get.yml')
    def get(self, meetup_id):
        """Fetch a single meetup item"""
        if meetup_id.isdigit():
            meetup_obj = MeetupModel()
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

    @jwt_required
    @swag_from('docs/meetup_delete.yml')
    def delete(self, meetup_id):
        """Delete a specific meetup"""
        meetup_obj = MeetupModel()
        if meetup_id.isdigit():
            user_obj = UserModel()
            current_user = get_jwt_identity()
            user = user_obj.find_user_by_username('username', current_user)
            if user['is_admin']:
                meetup = meetup_obj.get_meetup_by_id('id', int(meetup_id))
                if not meetup:
                    abort(404, {
                        "error": "Meetup with ID '{}' doesn't exist!".format(meetup_id),
                        "status": 404
                    })
                meetup_obj.delete_meetup_by_id('id', int(meetup_id))
                return {
                    'status': 200,
                    'message': "Meetup with ID '{}' has been successfully deleted".format(meetup_id)
                }, 200
            abort(403, {
                "error": "Only administrators can delete a meetup!",
                "status": 403
            })
        abort(400, {
            "error": "Meetup ID must be an Integer",
            "status": 400
        })
        return None


class UpcomingMeetup(Resource):
    """Request on an upcoming meetup item"""
    @jwt_required
    @swag_from('docs/meetup_get_all.yml')
    def get(self):
        """Fetch all upcoming meetups"""
        meetup_obj = MeetupModel()
        meetups = meetup_obj.get_all_meetups()
        if not meetups:
            abort(404, {
                "error": "No meetup is available",
                "status": 404
            })
        sorted_meetups = sorted(meetups, key=lambda item: item['happening_on'])
        return {
            'status': 200,
            'data': [MeetupModel.to_dict(meetup) for meetup in sorted_meetups]
        }, 200
