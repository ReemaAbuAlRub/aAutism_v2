import uuid
from sqlalchemy import Column, ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.sql import func
from app.db.base_class import Base

class Conversation(Base):
    id = Column(PGUUID(as_uuid=True), primary_key=True ,default=uuid.uuid4)
    user_id = Column(PGUUID(as_uuid=True), nullable=False) 
    role:str = Column(String, nullable=False)  
    message : str= Column(String, nullable=False )
    timestamp = Column(DateTime(timezone=True), server_default=func.now())