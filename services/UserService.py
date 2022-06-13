from typing import Optional

from sqlalchemy.orm import Session

from entities import User
from models.UserInfo import *


class UserService:
    def __init__(self, session: Session):
        self._session = session

    def create_user(self, user: UserCreateRequest):
        existing_user = self._session.query(User).where(User.email == user.email)
        if existing_user:
            raise Exception("User already exists")

        adding_user = User(email=user.email, name=user.name, password=user.password)
        self._session.add(adding_user)
        self._session.commit()

    def get_user_info(self, user_id: int) -> Optional[UserInfo]:
        user: User = self._session.query(User).get(user_id)
        if user is None:
            return None

        return UserInfo(user.id, user.name, user.email, user.winter_mode, len(user.plants))

    def authenticate(self, login: str, password: str) -> Optional[UserInfo]:
        user = self._session.query(User).where((User.email == login) & (User.password == password)).scalar()
        if not user:
            return None

        return UserInfo(user.id, user.name, user.email, user.winter_mode, len(user.plants))

