from flask import Blueprint, request, jsonify, g
from src.utils.jwt_bearer import token_required
from src.image.model import ImagePost
from src.database import db
from src.utils.error_handel import InstaCloneException
from flask_api import status

comment_images = Blueprint("comment_images", __name__)


@comment_images.route("/image_comment/<id>", methods=["POST"])
@token_required
def get_comment(id):
    """give comment on post"""
    
    if not id:
        raise InstaCloneException(
            message="ID not valid", status_code=status.HTTP_404_NOT_FOUND
        )
    
    comment_text = request.json.get("comment")
    image_data = ImagePost.query.filter(ImagePost.id == id).first()

    all_comments = image_data.comment.copy()
    new_comment = {g.user_data.id: comment_text}
    all_comments.append(new_comment)
    image_data.comment = all_comments
    db.session.commit()
    return jsonify(
        {
            "comment_text": comment_text, 
            "user_id": g.user_data.id
        },
    ), status.HTTP_200_OK
