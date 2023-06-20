from jose import jwt
from datetime import datetime, timedelta
from src.config import Config
from src.utils.error_handel import InstaCloneException
from flask_api import status
import jwt as jwt_error
from flask import request, g
from functools import wraps


def create_access_token(subject: dict, expire_time=timedelta(days=1)):
    if expire_time:
        expire_time = datetime.utcnow() + expire_time
    data = {**subject, "exp": expire_time}
    return jwt.encode(data, key=Config.JWT_SECRET_KEY, algorithm="HS256")


def create_refresh_token(subject: dict, expire_time=timedelta(days=7)):
    if expire_time:
        expire_time = datetime.utcnow() + expire_time
    data = {**subject, "exp": expire_time}
    return jwt.encode(data, key=Config.JWT_SECRET_KEY, algorithm="HS256")


def token_required(f):
    @wraps(f)
    def check_token(*args, **kwargs):
        try:
            bearer_token = request.headers.get('Authorization')
            token = bearer_token.split()[1]
            decode_token = jwt.decode(
                token=token, key=Config.JWT_SECRET_KEY, algorithms=["HS256"]
            )
            user = type("MyObject", (object,), decode_token)
            g.user_data = user
            if decode_token["exp"] >= datetime.timestamp(datetime.now()):
                return f(*args, **kwargs)
            else:
                raise InstaCloneException(
                    message="token is expired", status_code=status.HTTP_401_UNAUTHORIZED
                )
        except jwt_error.exceptions.InvalidTokenError:
            raise InstaCloneException(
                message="Invalid token", status_code=status.HTTP_401_UNAUTHORIZED
            )

    return check_token
