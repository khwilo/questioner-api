"""This module represents the comments view"""
from flask import abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import reqparse, Resource

from app.api.v2.models.comment_model import CommentsModel
from app.api.v2.models.question_model import QuestionModel
from app.api.v2.models.user_model import UserModel

class Comment(Resource):
    """Comments requests"""
    @jwt_required
    def post(self, question_id):
        '''Create a question record'''
        user_obj = UserModel()
        question_obj = QuestionModel()
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('comment', required=True, help="comment cannot be blank!")
        data = parser.parse_args()

        current_user = get_jwt_identity()
        user = user_obj.find_user_by_username('username', current_user)

        if not user:
            abort(401, {
                "error": "This action required loggin in!",
                "status": 401
            })

        comment = CommentsModel(
            comment=data['comment']
        )

        if question_id.isdigit():
            question = question_obj.get_question_by_id('id', int(question_id))
            if not question:
                abort(404, {
                    "error": "Question with id '{}' doesn't exist!".format(question_id),
                    "status": 404
                })
            comment.save(int(question_id), user['id'])
            return {
                'status': 201,
                'message': "Comment posted successfully!"
            }, 201
        abort(400, {
            "error": "Question ID must be an integer value",
            "status": 400
        })
        return None
