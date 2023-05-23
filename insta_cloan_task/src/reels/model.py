from src.database import db
from sqlalchemy import Column, String, Integer, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from src.utils.same_model import DBmodel
from src.user.model import User


class ReelsPost(db.Model, DBmodel):
    __tablename__ = "reels_post"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    reel_file = Column(String())
    caption = Column(String())
    uploaded_by = Column(ForeignKey(User.id))
    count_like = Column(Integer, default=0)
    liked_by = Column(JSON, default=[])
    comment = Column(JSON, default=[])
