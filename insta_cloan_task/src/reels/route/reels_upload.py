from flask import Blueprint, request, jsonify, g
import uuid
import os
from src.reels.model import ReelsPost
from src.database import db
from dotenv import load_dotenv
from src.utils.jwt_bearer import token_required
from src.follow.model import Follow
from src.utils.error_handel import InstaCloneException
from flask_api import status
from src.user.model import User
from src.utils.serializers import reel_serializer

reels_upload = Blueprint("reels_upload", __name__)

load_dotenv()


@reels_upload.route("/upload_reel", methods=["POST"])
@token_required
def upload_reel():
    """upload reel"""
    
    file = request.files["post_reel"]
    caption = request.form["caption"]
    if not file and caption:
        raise InstaCloneException(
            message="please fill all details", status_code=status.HTTP_400_BAD_REQUEST
        )
    old_file_name = file.filename
    split_file_name = old_file_name.split(".")
    file_name = str(uuid.uuid4()) + "." + split_file_name[-1]
    reel_path = os.environ.get("REEL_CREATE_PATH")
    directory_name = "user_reels"
    new_directory_path = os.path.join(reel_path, directory_name)

    if not os.path.exists(new_directory_path):
        os.makedirs(new_directory_path)

    save_path = os.path.join(new_directory_path, file_name)

    with open(save_path, "wb") as f:
        f.write(file.read())
        f.close()

    reel_data = ReelsPost(reel_file=file_name, caption=caption, uploaded_by=g.user_data.id)
    db.session.add(reel_data)
    db.session.commit()
    return jsonify(
        {
            "id": reel_data.id,
            "filename": reel_data.reel_file,
            "caption": reel_data.caption,
        },
    ), status.HTTP_200_OK


@reels_upload.route("/all_reels/<id>", methods=["GET"])
@token_required
def get_all_reels(id):
    """get all reels"""
    
    if not id:
        raise InstaCloneException(
            message="ID not valid", status_code=status.HTTP_404_NOT_FOUND
        )
    follow = Follow.query.filter(Follow.following == g.user_data.id).first()
    if not follow:
        raise InstaCloneException(
            message="you are not following", status_code=status.HTTP_404_NOT_FOUND
        )
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    reel_data = ReelsPost.query.filter(ReelsPost.uploaded_by == g.user_data.id).paginate(
        page=page, per_page=per_page
    )

    return jsonify(
            reel_serializer(reel_data),
        ), status.HTTP_200_OK,


@reels_upload.route("/get_reel/<id>", methods=["GET"])
@token_required
def get_reel(id):
    """get reel"""
    
    if not id:
        raise InstaCloneException(
            message="ID not valid", status_code=status.HTTP_404_NOT_FOUND
        )
    reels_data = ReelsPost.query.get(id)
    follow = Follow.query.filter(Follow.following == g.user_data.id).first()
    if not follow:
        raise InstaCloneException(
            message="you are not following", status_code=status.HTTP_404_NOT_FOUND
        )
    return {
        "id": reels_data.id,
        "file_name": reels_data.reel_file,
        "caption": reels_data.caption,
        "likes": reels_data.count_like,
        "liked_by": reels_data.liked_by,
        "comment": reels_data.comment,
    }, status.HTTP_200_OK


@reels_upload.route("/del_reel/<id>", methods=["DELETE"])
@token_required
def del_reel(id):
    """delete reel"""
    
    if not id:
        raise InstaCloneException(
            message="ID not valid", status_code=status.HTTP_404_NOT_FOUND
        )
    reels_data = ReelsPost.query.get(id)
    reel_name = reels_data.reel_file

    path = os.environ.get("REEL_DELETE_PATH")
    if reel_name:
        os.remove(os.path.join(path, reel_name))
        db.session.delete(reels_data)
        db.session.commit()
        return jsonify(
            message="reels deleted successfully", status_code=status.HTTP_200_OK
        )
    else:
        raise InstaCloneException(
            message="No filename provided", status_code=status.HTTP_204_NO_CONTENT
        )
