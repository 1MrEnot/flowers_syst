from typing import Iterable

from sqlalchemy.orm import Session

from entities import User, Plant, Measurement
from models import *


class Repository:
    def __init__(self, session: Session):
        self._session = session

    def create_user(self, user: UserCreateRequest):
        existing_user = self._session.query(User).where(User.email == user.email).scalar()
        if existing_user:
            raise Exception("User already exists")

        adding_user = User(email=user.email, name=user.name, password=user.password)
        self._session.add(adding_user)
        self._session.commit()

    def get_user_info(self, user_id: int) -> Optional[UserInfo]:
        user: User = self._session.query(User).get(user_id)
        if not user:
            return None

        return Repository._map_user_model(user)

    def authenticate(self, login: str, password: str) -> Optional[UserInfo]:
        user = self._session.query(User).where((User.email == login) & (User.password == password)).scalar()
        if not user:
            return None

        return Repository._map_user_model(user)

    def get_plant_info(self, plant_id: int) -> PlantInfo:
        plant: Plant = self._session.query(Plant).get(plant_id)
        plant_measurements: Iterable[Measurement] = self._session.query(Measurement).where(Measurement.plant_id == plant_id)
        measurements = [Moisture(m.value, m.timestamp) for m in plant_measurements]
        return PlantInfo(plant_id, measurements, min_moisture=plant.min_moisture)

    @staticmethod
    def _next_watering_days(next_watering_datetime: Optional[datetime]) -> Optional[int]:
        if next_watering_datetime is None:
            return None

        return (next_watering_datetime - datetime.now()).days

    @staticmethod
    def _map_plant_model(p: Plant) -> PlantModel:
        return PlantModel(p.id, p.name, p.average_cycle, Repository._next_watering_days(p.next_watering))

    @staticmethod
    def _map_user_model(user: User) -> UserInfo:
        plants = [Repository._map_plant_model(p) for p in user.plants]
        return UserInfo(user.id, user.name, user.email, user.winter_mode, plants)
