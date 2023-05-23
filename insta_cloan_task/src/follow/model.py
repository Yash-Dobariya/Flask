from src.database import db
from sqlalchemy import Column, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from src.user.model import User


class Follow(db.Model):
    __tablename__ = "follow"
    """follow model"""

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    following = Column(ForeignKey(User.id))
    follower = Column(ForeignKey(User.id))
    is_delete = Column(Boolean, default=False)
