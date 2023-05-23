from flask import Blueprint, request, jsonify, g
from src.utils.jwt_bearer import token_required
from src.story.model import Story
from src.database import db
from src.utils.error_handel import InstaCloneException
from flask_api import status

story_comments = Blueprint("story_reels", __name__)


@story_comments.route("/story_comment/<id>", methods=["POST"])
@token_required
def add_comment(id):
    """story comment"""
    
    if not id:
        raise InstaCloneException(
            message="ID not valid", status_code=status.HTTP_404_NOT_FOUND
        )
    
    comment_text = request.json.get("comment")
    story = Story.query.filter(Story.id == id).first()

    all_comments = story.comment.copy()
    new_comment = {g.user_data.id: comment_text}
    all_comments.append(new_comment)
    story.comment = all_comments
    db.session.commit()
    return jsonify(
        {
            "comment_text": comment_text,
            "user_id": g.user_data.id,
        },
    ), status.HTTP_200_OK,
