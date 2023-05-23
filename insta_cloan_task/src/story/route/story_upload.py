from flask import Blueprint, request, jsonify, g
from src.utils.jwt_bearer import token_required
from src.story.model import Story
from src.database import db
from src.utils.error_handel import InstaCloneException
from flask_api import status
from src.user.model import User
from src.utils.serializers import story_serializer

add_story = Blueprint("add_story", __name__)


@add_story.route("/story", methods=["POST"])
@token_required
def upload_story():
    """Add story"""
    
    story_file = request.files["post_story"]
    filename = story_file.filename

    story_data = Story(add_story=filename, uploaded_by=g.user_data.id)
    db.session.add(story_data)
    db.session.commit()
    return jsonify(
        {
            "id": story_data.id
        },
    ), status.HTTP_200_OK


@add_story.route("/all_story/<id>", methods=["GET"])
@token_required
def all_story(id):
    """get all story"""
    
    if not id:
        raise InstaCloneException(
            message="ID not valid", status_code=status.HTTP_404_NOT_FOUND
        )
    page = request.args.get("page", 1, type=int)
    story_data = Story.query.filter(Story.uploaded_by == id).paginate(
        page=page, per_page=1
    )

    return jsonify(story_serializer(story_data)), status.HTTP_200_OK,


@add_story.route("/del_story/<id>", methods=["DELETE"])
@token_required
def delete_story(id):
    """delete story"""
    
    if not id:
        raise InstaCloneException(
            message="ID not valid", status_code=status.HTTP_404_NOT_FOUND
        )
    story = Story.query.filter(Story.id == id).first()
    db.session.delete(story)
    db.session.commit()
    return jsonify(message="reels deleted successfully", status_code=status.HTTP_200_OK)
