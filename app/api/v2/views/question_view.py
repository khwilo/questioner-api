"""This module represents the question view"""
from flask import abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import reqparse, Resource

from flasgger import swag_from

from app.api.v2.models.meetup_model import MeetupModel
from app.api.v2.models.user_model import UserModel
from app.api.v2.models.question_model import QuestionModel

class Question(Resource):
    """Question requests"""
    @jwt_required
    @swag_from('docs/question_post.yml')
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
    @swag_from('docs/question_upvote.yml')
    def patch(self, question_id):
        """Increase the vote of a question by 1"""
        if question_id.isdigit():
            question_obj = QuestionModel()
            question = question_obj.get_question_by_id('id', int(question_id))
            if not question:
                abort(404, {
                    "error": "Question with ID '{}' doesn't exist!".format(question_id),
                    "status": 404
                })
            question_obj.vote_question("upvote", int(question_id))
            updated_question = question_obj.get_question_by_id('id', int(question_id))
            return {
                "status": 200,
                "data": [
                    {
                        "title": updated_question["title"],
                        "body": updated_question["body"],
                        "votes": updated_question["votes"]
                    }
                ]
            }, 200
        abort(400, {
            "error": "Question ID must be an integer value",
            "status": 400
        })
        return None
