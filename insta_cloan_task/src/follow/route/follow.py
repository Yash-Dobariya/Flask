from flask import Blueprint, jsonify, g
from src.follow.model import Follow
from src.utils.jwt_bearer import token_required
from src.database import db
from src.user.model import UserMetaData
from src.utils.error_handel import InstaCloneException
from flask_api import status

follow_user = Blueprint("follow_user", __name__)


@follow_user.route("/following/<id>", methods=["GET"])
@token_required
def follow_by_user(id):
    """user can follow another user"""

    follow = Follow.query.filter(Follow.following == id).first()

    if not id:
        raise InstaCloneException(
            message="ID not valid", status_code=status.HTTP_404_NOT_FOUND
        )

    if follow is None or follow.is_delete == True:
        current_user_meta = UserMetaData.query.filter_by(id=g.user_data.id).first()

        if current_user_meta is None:
            current_user_meta = UserMetaData(id=g.user_data.id)
            db.session.add(current_user_meta)
            db.session.commit()

        if follow is None:
            new_follow = Follow(following=id, follower=g.user_data.id)
            db.session.add(new_follow)
            db.session.commit()
        elif follow.is_delete == True:
            follow.is_delete = False
            db.session.commit()

        # current_user_meta.following += 1
        current_user_meta.follower += 1
        db.session.commit()
        return jsonify(
            message="you follow {}".format(id),
            status_code=status.HTTP_200_OK,
        )
    else:
        follow.is_delete = True
        db.session.commit()
        meta_data = UserMetaData.query.filter_by(id=g.user_data.id).first()
        # meta_data.following -= 1
        meta_data.follower -= 1
        db.session.commit()
        return jsonify(
            message="{} unfollowed".format(id),
            status_code=status.HTTP_200_OK,
        )


@follow_user.route("/follow/<id>", methods=["GET"])
@token_required
def follow_count(id):
    """retrieve the follower and following count for a user"""
    
    if not id:
        raise InstaCloneException(
            message="ID not valid", status_code=status.HTTP_404_NOT_FOUND
        )

    follow_data = UserMetaData.query.filter(UserMetaData.id == g.user_data.id).first()
    return jsonify(
        message={"follower": follow_data.follower, "following": follow_data.following},
        status_code=status.HTTP_404_NOT_FOUND,
    )
