import dataclasses
from datetime import datetime
from typing import Optional


@dataclasses.dataclass
class PlantModel:
    p_id: int
    name: str
    average_cycle: Optional[float]
    next_watering: Optional[float]
    winter_mode: bool = False


@dataclasses.dataclass
class Moisture:
    value: float
    timestamp: datetime


@dataclasses.dataclass
class PlantInfo:
    p_id: int
    measurements: list[Moisture]
    forecast: list[Moisture] = dataclasses.field(default_factory=list)
    min_moisture: float = 0


@dataclasses.dataclass
class UserInfo:
    u_id: int
    name: str
    email: str
    is_winter_mode: bool
    plants: list[PlantModel]


@dataclasses.dataclass
class UserCreateRequest:
    name: str
    email: str
    password: str
