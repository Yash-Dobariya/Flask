from flask import Blueprint, jsonify, g
from src.image.model import ImagePost
from src.utils.jwt_bearer import token_required
from src.database import db
from src.utils.error_handel import InstaCloneException
from flask_api import status

like_images = Blueprint("like_images", __name__)


@like_images.route("/image_like/<id>", methods=["GET"])
@token_required
def like_count(id):
    """give like on particular image"""
    
    if not id:
        raise InstaCloneException(
            message="ID not valid", status_code=status.HTTP_404_NOT_FOUND
        )

    image_data = ImagePost.query.filter(ImagePost.id == id).first()
    likes = image_data.count_like
    liked_by = image_data.liked_by.copy()

    """user take_back like"""
    if liked_by is not None and g.user_data.id in liked_by:
        liked_by.remove(g.user_data.id)
        if likes > 0:
            likes -= 1
    else:
        """Give like"""
        liked_by.append(g.user_data.id)
        likes += 1

    image_data.count_like = likes
    image_data.liked_by = liked_by
    db.session.commit()
    
    return jsonify({"like": likes, "liked_by": liked_by}), status.HTTP_200_OK
