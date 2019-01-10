'''This module represents the question view'''
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import reqparse, Resource

from app.api.v1.models.meetup_model import MeetupModel
from app.api.v1.models.user_model import UserModel
from app.api.v1.models.question_model import QuestionModel

class Question(Resource):
    '''Question requests'''
    @jwt_required
    def post(self, meetup_id):
        '''Create a question record'''
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True, help="title cannot be blank!")
        parser.add_argument('body', required=True, help="body cannot be blank!")
        data = parser.parse_args()

        current_user = get_jwt_identity()
        user = UserModel.get_user_by_username(current_user)

        if not user:
            return {
                'message': "This action required loggin in!"
            }, 401

        question = QuestionModel(
            created_by=user['user_id'],
            meetup=meetup_id,
            title=data['title'],
            body=data['body']
        )

        if meetup_id.isdigit():
            meetup = MeetupModel.get_meetup_by_id(int(meetup_id))
            if meetup == {}:
                return {
                    'message': "Meetup with id '{}' doesn't exist!".format(meetup_id)
                }, 404
            QuestionModel.add_question(question, meetup_id)
            return {
                'status': 201,
                'data': [meetup]
            }, 201
        return {
            'message': 'meetup ID must be an integer value'
        }, 400
