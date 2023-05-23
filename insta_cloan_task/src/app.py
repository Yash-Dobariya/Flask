from src.user.route import user_app
from flask import Flask, jsonify
from dotenv import load_dotenv
import os, sys
from src.database import db
from flask_jwt_extended import JWTManager
from src.image.route.image_upload import image_upload
from src.image.route.image_like import like_images
from src.image.route.image_comment import comment_images
from src.reels.route.reels_upload import reels_upload
from src.reels.route.reels_like import like_reels
from src.reels.route.reels_comment import comment_reels
from src.story.route.story_upload import add_story
from src.story.route.story_like import like_story
from src.story.route.story_comment import story_comments
from src.message.route.message_send import send_message
from src.follow.route.follow import follow_user
from src.utils.error_handel import InstaCloneException
import traceback, psycopg2
from flask_api import status
from src.config import Config


def create_app():
    load_dotenv()

    app = Flask(__name__)

    app.config.from_object(Config)

    app.config["SECRET_KEY"] = os.environ.get("SECRET")

    db.init_app(app)

    app.register_blueprint(user_app)
    app.register_blueprint(image_upload)
    app.register_blueprint(like_images)
    app.register_blueprint(comment_images)
    app.register_blueprint(reels_upload)
    app.register_blueprint(like_reels)
    app.register_blueprint(comment_reels)
    app.register_blueprint(add_story)
    app.register_blueprint(like_story)
    app.register_blueprint(story_comments)
    app.register_blueprint(send_message)
    app.register_blueprint(follow_user)

    @app.errorhandler(Exception)
    def handle_known_exceptions(exception: Exception):
        app.logger.error(traceback.format_exc())

        if isinstance(exception, InstaCloneException):
            return (jsonify(message=exception.message), exception.status_code)

        return (
            jsonify(message="Something went wrong!!", error=str(exception)),
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    JWTManager(app)

    return app


main_app = create_app()
