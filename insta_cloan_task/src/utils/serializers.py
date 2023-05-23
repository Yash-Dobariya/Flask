"""User serializer"""

def all_user_serializer(all_user):
    result = []
    for user in all_user:
        result.append(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email_id": user.email_id,
                "dob": user.dob,
                "country": user.country,
            }
        )
    return result


def user_serializer(user):
    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email_id": user.email_id,
        "dob": user.dob,
        "country": user.country,
        "bio": user.bio,
    }


"""Image serializer"""


def image_serializer(image_data):
    result = []
    for image in image_data:
        result.append(
            {
                "id": image.id,
                "filename": image.img_filename,
                "caption": image.caption,
                "count_like": image.count_like,
                "liked_by": image.liked_by,
                "comment": image.comment,
            }
        )
    return result


"""Reel serializer"""


def reel_serializer(reel_data):
    result = []
    for reel in reel_data:
        result.append(
            {
                "id": reel.id,
                "file_name": reel.reel_file,
                "caption": reel.caption,
                "likes": reel.count_like,
                "liked_by": reel.liked_by,
                "comment": reel.comment,
            }
        )
    return result


"""Story serializer"""


def story_serializer(story_data):
    result = []
    for story in story_data:
        result.append(
            {
                "id": story.id,
                "story": story.add_story,
                "likes": story.count_like,
                "like_by": story.liked_by,
                "comment": story.comment,
            }
        )
    return result


"""Message serializer"""


def message_receive_serializer(message_data):
    result = []
    for msg in message_data:
        result.append(
            {"sender_id": msg.sender_id, "message": msg.message, "sent_at": msg.send_at}
        )
    return result


def message_sending_serializer(message_data):
    result = []
    for msg in message_data:
        result.append(
            {
                "id": msg.id,
                "sender_id": msg.message_receive,
                "message": msg.message,
                "sent_at": msg.send_at,
            }
        )
    return result
