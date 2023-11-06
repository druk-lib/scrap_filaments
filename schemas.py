from typing import List

from pydantic import BaseModel

class Filament(BaseModel):
    name: str
    type: str
    weight: float
    price: float
    color: str
    url: str
    update_time: int


class Manufacturer(BaseModel):
    name: str
    filaments: List[Filament] = []


class Manufacturers(BaseModel):
    manufacturers: List[Manufacturer] = []
