from src.database import db
from sqlalchemy import Column, String, Date, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from src.utils.same_model import DBmodel


class User(db.Model, DBmodel):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    first_name = Column(String())
    last_name = Column(String())
    email_id = Column(String(), unique=True)
    password = Column(String())
    dob = Column(Date)
    country = Column(String())
    bio = Column(String())


class UserMetaData(db.Model):
    __tablename__ = "usermetadata"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    follower = Column(Integer, default=0)
    following = Column(Integer, default=0)
    extra = Column(JSON)
