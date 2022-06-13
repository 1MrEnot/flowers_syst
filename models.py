from typing import Optional
import dataclasses


@dataclasses.dataclass
class PlantModel:
    p_id: int
    name: str
    average_cycle: Optional[float]
    next_watering: Optional[float]


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
