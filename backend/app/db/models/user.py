from datetime import datetime
from sqlalchemy import Column, Integer, Text, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from ...db.base_class import Base
import uuid

class User(Base):
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4,unique=True,nullable=False)
    email= Column(String, nullable=False, unique=True)
    password= Column(String, nullable=False)
    is_active=Column(Boolean,default=True)
