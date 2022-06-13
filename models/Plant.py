import dataclasses
from typing import Optional


@dataclasses.dataclass
class PlantModel:
    name: str
    average_cycle: Optional[int]
    next_watering: Optional[int]
