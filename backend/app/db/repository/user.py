# from sqlalchemy.orm import Session
# from schemas.user import UserCreate
# from db.models.users import User


# def create_new_user(user: UserCreate, db:Session) -> User:
#     user=User(email=user.email,password=user.password,is_active=True)
#     db.add(user)
#     db.commit()
#     db.refresh(user)

#     return user