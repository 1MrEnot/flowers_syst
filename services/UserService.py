import dataclasses

from entities import User

from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class UserService:
    def __init__(self, session: Session):
        self._session = session

    def get_user(self, user_id: int):
        return self._session.query(User).get(user_id)

    def create_user(self, user: User):
        self._session.add(user)
        self._session.commit()

    def get_user_info(self, user_id):
        user = self._session.query(User).get(user_id)
        return UserInfo(None, None, None, None)
        # return UserInfo("<USERNAME>", user.email, user.winter_mode, len(user.plants))


@dataclasses.dataclass
class UserInfo:
    name: str
    email: str
    is_winter_mode: bool
    plant_count: int


if __name__ == '__main__':
    eng = create_engine("sqlite:///../test.db", echo=True, future=True)
    with Session(eng) as session:
        serv = UserService(session)
        user = User(email="new_user@foo.com", password="pass", winter_mode=True)
        serv.create_user(user)
