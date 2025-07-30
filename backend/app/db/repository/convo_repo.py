# app/db/repositories/convo_repo.py
from typing import List
from sqlalchemy.orm import Session
from app.db.models.conversation import Conversation

class ConversationRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, convo: Conversation) -> Conversation:
        self.db.add(convo)
        self.db.commit()
        self.db.refresh(convo)
        return convo

    def add_user_message(self, user_id: str, message: str) -> Conversation:
        convo = Conversation(user_id=user_id, role="user", message=message)
        return self.add(convo)

    def add_assistant_message(self, user_id: str, message: str) -> Conversation:
        convo = Conversation(user_id=user_id, role="assistant", message=message)
        return self.add(convo)

    def list_by_user(self, user_id: str) -> List[Conversation]:
        return (
            self.db.query(Conversation)
            .filter(Conversation.user_id == user_id)
            .order_by(Conversation.timestamp)
            .all()
        )
