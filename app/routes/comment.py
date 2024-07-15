from flask import request, jsonify
from flask_restx import Resource, Namespace
from ..extensions import db
from ..models.comment import Comment
from ..schemas.comment_schemas import comment_request_model, comment_response_model
from flask_jwt_extended import jwt_required
from ..utils.utils import token_required

comment_namespace = Namespace('comments', description='Comment related operations')

def register_comment_routes(api):
    api.add_namespace(comment_namespace)

@comment_namespace.route('')
class CommentList(Resource):
    @token_required
    @comment_namespace.marshal_list_with(comment_response_model)
    @comment_namespace.doc(description='Get the list of all Comments')
    def get(self):
        return Comment.query.all()

    @token_required
    @comment_namespace.expect(comment_request_model, validate=True)
    @comment_namespace.doc(description='Create a new Comment')
    def post(self):
        data = request.get_json()
        new_comment = Comment(
            comment=data['comment'],
            attachment_url=data.get('attachment_url'),
            servicerequest_id=data['servicerequest_id'],
            employee_id=data['employee_id']
        )
        db.session.add(new_comment)
        db.session.commit()
        return {'message': 'Comment created successfully'}, 201

@comment_namespace.route('/<int:id>')
class CommentResource(Resource):
    @token_required
    @comment_namespace.marshal_with(comment_response_model)
    @comment_namespace.doc(description='Get details of a specific Comment by ID')
    def get(self, id):
        comment = Comment.query.get_or_404(id)
        return comment

    @token_required
    @comment_namespace.expect(comment_request_model, validate=True)
    @comment_namespace.doc(description='Update details of a specific Comment by ID')
    def put(self, id):
        data = request.get_json()
        comment = Comment.query.get_or_404(id)
        comment.comment = data['comment']
        comment.attachment_url = data.get('attachment_url', comment.attachment_url)
        comment.servicerequest_id = data['servicerequest_id']
        comment.employee_id = data['employee_id']
        db.session.commit()
        return {'message': 'Comment updated successfully'}

    @token_required
    @comment_namespace.doc(description='Delete a specific Comment by ID')
    def delete(self, id):
        comment = Comment.query.get_or_404(id)
        db.session.delete(comment)
        db.session.commit()
        return {'message': 'Comment deleted successfully'}