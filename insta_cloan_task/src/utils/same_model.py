from sqlalchemy import Column, DateTime, String, Boolean
from datetime import datetime

class DBmodel:

    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())
    updated_by = Column(String(256))
    is_active = Column(Boolean, default=True)
