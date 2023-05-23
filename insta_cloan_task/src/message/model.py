from src.database import db
from sqlalchemy import Column, String, ForeignKey, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from src.user.model import User
from datetime import datetime


class Message(db.Model):
    __tablename__ = "message"
    """message model"""

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    message = Column(String())
    sender_id = Column(ForeignKey(User.id))
    message_receive = Column(ForeignKey(User.id))
    send_at = Column(DateTime, default=datetime.utcnow())
