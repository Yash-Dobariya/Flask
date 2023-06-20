from flask import Blueprint, request, jsonify, g
from src.message.model import Message
from src.database import db
from src.utils.jwt_bearer import token_required
from src.follow.model import Follow
from src.utils.error_handel import InstaCloneException
from flask_api import status
from src.utils.serializers import message_sending_serializer, message_receive_serializer

send_message = Blueprint("send_message", __name__)


@send_message.route("/message_sending/<id>", methods=["POST"])
@token_required
def message_send(id):
    """send message"""

    if not id:
        raise InstaCloneException(
            message="ID not valid", status_code=status.HTTP_404_NOT_FOUND
        )

    follow = Follow.query.filter(Follow.following == g.user_data.id).first()
    if not follow:
        raise InstaCloneException(
            message="you are not following", status_code=status.HTTP_404_NOT_FOUND
        )

    messages = request.json.get("send")
    send_messages = Message(
        message=messages, sender_id=g.user_data.id, message_receive=id
    )
    db.session.add(send_messages)
    db.session.commit()
    return (
        jsonify(
            {
                "id": send_messages.id,
                "message": send_messages.message,
                "send_at": send_messages.send_at,
            }
        ),
        status.HTTP_200_OK,
    )


@send_message.route("/send_post/<id>", methods=["POST"])
@token_required
def post_send(id):
    """send any image video in local"""

    if not id:
        raise InstaCloneException(
            message="ID not valid", status_code=status.HTTP_404_NOT_FOUND
        )

    follow = Follow.query.filter(Follow.following == g.user_data.id).first()
    if not follow:
        raise InstaCloneException(
            message="you are not following", status_code=status.HTTP_404_NOT_FOUND
        )

    send_file = request.files["send"]
    file_name = send_file.filename
    send_messages = Message(
        message=file_name, sender_id=g.user_data.id, message_receive=id
    )
    db.session.add(send_messages)
    db.session.commit()
    return (
        jsonify(
            {
                "id": send_messages.id,
                "message": send_messages.message,
                "send_at": send_messages.send_at,
            }
        ),
        status.HTTP_200_OK,
    )


@send_message.route("/message_send", methods=["GET"])
@token_required
def show_message_send():
    """send messages"""

    message_data = Message.query.filter(Message.sender_id == g.user_data.id).all()
    return jsonify(
        message=message_sending_serializer(message_data), status_code=status.HTTP_200_OK
    )


@send_message.route("/message_receive", methods=["GET"])
@token_required
def message_receive():
    """message receive"""

    message_data = Message.query.filter(Message.message_receive == g.user_data.id).all()
    return jsonify(
        message=message_receive_serializer(message_data), status_code=status.HTTP_200_OK
    )


@send_message.route("/del_message/<id>", methods=["DELETE"])
@token_required
def del_message(id):
    """delete message"""

    if not id:
        raise InstaCloneException(
            message="ID not valid", status_code=status.HTTP_404_NOT_FOUND
        )
    message_data = Message.query.filter(Message.id == id).first()
    db.session.delete(message_data)
    db.session.commit()
    return jsonify(message="Successfully delete", status_code=status.HTTP_200_OK)
