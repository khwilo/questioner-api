"""This module represents the question view"""
from flask import abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import reqparse, Resource

from app.api.v2.models.meetup_model import MeetupModel
from app.api.v2.models.user_model import UserModel
from app.api.v2.models.question_model import QuestionModel

class Question(Resource):
    """Question requests"""
    @jwt_required
    def post(self, meetup_id):
        '''Create a question record'''
        user_obj = UserModel()
        meetup_obj = MeetupModel()
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('title', required=True, help="title cannot be blank!")
        parser.add_argument('body', required=True, help="body cannot be blank!")
        data = parser.parse_args()

        current_user = get_jwt_identity()
        user = user_obj.find_user_by_username('username', current_user)

        if not user:
            abort(401, {
                "error": "This action required loggin in!",
                "status": 401
            })

        question = QuestionModel(
            title=data['title'],
            body=data['body']
        )

        if meetup_id.isdigit():
            meetup = meetup_obj.get_meetup_by_id('id', int(meetup_id))
            if not meetup:
                abort(404, {
                    "error": "Meetup with id '{}' doesn't exist!".format(meetup_id),
                    "status": 404
                })
            question.save(user['id'], int(meetup_id))
            return {
                'status': 201,
                'message': "Question created successfully!"
            }, 201
        abort(400, {
            "error": "Meetup ID must be an integer value",
            "status": 400
        })
        return None

class Upvote(Resource):
    """Upvotes requests"""
    @jwt_required
    def patch(self, meetup_id, question_id):
        """
        '''Increase the vote of a question by 1'''
        meetup = MeetupModel.get_meetup_by_id(int(meetup_id))
        if meetup == {}:
            abort(404, {
                "error": "Meetup with ID '{}' doesn't exist!".format(meetup_id),
                "status": 404
            })
        question = MeetupModel.get_question_by_id(meetup, int(question_id))
        if question == {}:
            abort(404, {
                "error": "Question with ID '{}' doesn't exist!".format(question_id),
                "status": 404
            })
        question["votes"] += 1
        return {
            "status": 200,
            "data": [
                {
                    "meetup": meetup_id,
                    "title": question["title"],
                    "body": question["body"],
                    "votes": question["votes"]
                }
            ]
        }, 200
    """

class Downvote(Resource):
    """Downvotes requests"""
    @jwt_required
    def patch(self, meetup_id, question_id):
        """
        '''Decrease the vote of a question by 1'''
        meetup = MeetupModel.get_meetup_by_id(int(meetup_id))
        if meetup == {}:
            abort(404, {
                "error": "Meetup with ID '{}' doesn't exist!".format(meetup_id),
                "status": 404
            })
        question = MeetupModel.get_question_by_id(meetup, int(question_id))
        if question == {}:
            abort(404, {
                "error": "Question with ID '{}' doesn't exist!".format(question_id),
                "status": 404
            })
        question["votes"] -= 1
        return {
            "status": 200,
            "data": [
                {
                    "meetup": meetup_id,
                    "title": question["title"],
                    "body": question["body"],
                    "votes": question["votes"]
                }
            ]
        },
    """
