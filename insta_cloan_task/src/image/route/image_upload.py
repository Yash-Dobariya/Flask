from flask import Blueprint, request, jsonify, g
from src.image.model import ImagePost
from src.database import db
import os
import uuid
from dotenv import load_dotenv
from src.utils.jwt_bearer import token_required
from src.follow.model import Follow
from src.utils.error_handel import InstaCloneException
from flask_api import status
from src.utils.serializers import image_serializer

image_upload = Blueprint("image_upload", __name__)

load_dotenv()

@image_upload.route("/upload_image", methods=["POST"])
@token_required
def upload_image():
    """upload image on insta_clone"""

    file = request.files["post_image"]
    caption = request.form["caption"]

    if not file and caption:
        raise InstaCloneException(
            message="please fill all details", status_code=status.HTTP_400_BAD_REQUEST
        )

    old_file_name = file.filename
    split_file_name = old_file_name.split(".")
    id = str(uuid.uuid4())
    file_name = id + "." + split_file_name[-1]
    image_path = os.environ.get("IMAGE_CREATE_PATH")
    directory_name = "user_images"
    new_directory_path = os.path.join(image_path, directory_name)

    if not os.path.exists(new_directory_path):
        os.makedirs(new_directory_path)

    save_path = os.path.join(new_directory_path, file_name)

    with open(save_path, "wb") as f:
        f.write(file.read())
        f.close()

    image_data = ImagePost(
        img_filename=file_name, caption=caption, uploaded_by=g.user_data.id
    )
    db.session.add(image_data)
    db.session.commit()
    return (
        jsonify(
            {
                "id": image_data.id,
                "filename": image_data.img_filename,
                "caption": image_data.caption,
            },
        ),
        status.HTTP_200_OK,
    )


"""get all image uploaded user"""


@image_upload.route("/all_image/<id>", methods=["GET"])
@token_required
def get_all_image(id):
    """get all image uploaded by user"""
    
    if not id:
        raise InstaCloneException(
            message="ID not valid", status_code=status.HTTP_404_NOT_FOUND
        )

    follow = Follow.query.filter(Follow.following == g.user_data.id).first()
    if not follow:
        raise InstaCloneException(
            message="you are not following", status_code=status.HTTP_200_OK
        )

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    image_data = ImagePost.query.filter(ImagePost.uploaded_by == id).paginate(
        page=page, per_page=per_page
    )
    return jsonify(image_serializer(image_data)), status.HTTP_200_OK



@image_upload.route("/get_image/<id>", methods=["GET"])
@token_required
def get_image(id):
    """get one image uploaded by user"""
    
    if not id:
        raise InstaCloneException(
            message="ID not valid", status_code=status.HTTP_404_NOT_FOUND
        )

    follow = Follow.query.filter(Follow.following == g.user_data.id).first()
    if not follow:
        raise InstaCloneException(
            message="you are not following", status_code=status.HTTP_404_NOT_FOUND
        )

    image_data = ImagePost.query.get(id)
    return (
        jsonify(
            {
                "id": image_data.id,
                "image": image_data.img_filename,
                "caption": image_data.caption,
                "likes": image_data.count_like,
                "liked_by": image_data.liked_by,
                "comment": image_data.comment,
            }
        ),
        status.HTTP_200_OK,
    )


"""delete image"""


@image_upload.route("/del_image/<id>", methods=["DELETE"])
@token_required
def update_image(id):
    """delete image"""
    
    if not id:
        raise InstaCloneException(
            message="ID not valid", status_code=status.HTTP_404_NOT_FOUND
        )

    image_data = ImagePost.query.get(id)
    image_file_name = image_data.img_filename
    path = os.environ.get("IMAGE_DELETE_PATH")
    
    if image_file_name:
        os.remove(os.path.join(path, image_file_name))
        db.session.delete(image_data)
        db.session.commit()
        return jsonify(
            message="Image deleted successfully", status_code=status.HTTP_200_OK
        )
    else:
        raise InstaCloneException(
            message="No filename provided", status_code=status.HTTP_204_NO_CONTENT
        )
