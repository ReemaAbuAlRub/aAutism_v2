from datetime import datetime
from sqlalchemy import Column, Integer, Text, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.base_class import Base

class User(Base):
    id = Column(Integer, primary_key=True)
    email= Column(String, nullable=False, unique=True)
    password= Column(String, nullable=True)
    is_active=Column(Boolean,default=True)
