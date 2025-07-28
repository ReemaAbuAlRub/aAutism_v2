from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
from ..core.config import settings

dburl=settings.DATABASE_URL

engine=create_engine(dburl)
session_local=sessionmaker(autoflush=False,autocommit=False,bind=engine)

def get_db() -> Generator:
    try:
         db=session_local()
         yield db
    finally:
        db.close()