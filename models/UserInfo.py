import dataclasses


@dataclasses.dataclass
class UserInfo:
    u_id: int
    name: str
    email: str
    is_winter_mode: bool
    plant_count: int


@dataclasses.dataclass
class UserCreateRequest:
    name: str
    email: str
    password: str
