from flask import Blueprint, request, jsonify, g
from src.utils.jwt_bearer import token_required
from src.reels.model import ReelsPost
from src.database import db
from src.utils.error_handel import InstaCloneException
from flask_api import status

comment_reels = Blueprint("comment_reels", __name__)


@comment_reels.route("/reel_comment/<id>", methods=["POST"])
@token_required
def get_comments(id):
    """reel_comment"""
    
    if not id:
        raise InstaCloneException(
            message="ID not valid", status_code=status.HTTP_404_NOT_FOUND
        )

    comment_text = request.json.get("comment")
    reels_data = ReelsPost.query.filter(ReelsPost.id == id).first()

    all_comments = reels_data.comment.copy()
    new_comment = {g.user_data.id: comment_text}
    all_comments.append(new_comment)
    reels_data.comment = all_comments
    db.session.commit()
    return (
        jsonify(
            {
                "comment_text": comment_text,
                "user_id": g.user_data.id,
            }
        ),
        status.HTTP_200_OK,
    )
