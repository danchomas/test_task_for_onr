from sqlalchemy.orm import Session
from models.user_models import User
from schemas.user_schemas import UserCreateSchema
from fastapi import HTTPException, status


class UserCreateManager:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreateSchema) -> User:
        existing_user = (
            self.db.query(User)
            .filter((User.email == user.email) | (User.username == user.username))
            .first()
        )

        if existing_user:
            if existing_user.email == user.email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered",
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken",
                )
        db_user = User(email=user.email, username=user.username, password=user.password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user


class UserLoginManager:
    def __init__(self, db: Session):
        self.db = db

    def login_user(self, username: str, password: str) -> User:
        user = self.db.query(User).filter(User.username == username).first()
        if user and user.password == password:
            return user
        return None