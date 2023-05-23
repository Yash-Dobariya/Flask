from src.database import db
from sqlalchemy import Column, String, ForeignKey, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSON
import uuid
from src.user.model import User
from datetime import datetime


class Story(db.Model):
    __tablename__ = "story"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    add_story = Column(String())
    uploaded_by = Column(ForeignKey(User.id))
    count_like = Column(Integer, default=0)
    liked_by = Column(JSON, default=[])
    comment = Column(JSON, default=[])
    created_at = Column(DateTime, default=datetime.utcnow())
