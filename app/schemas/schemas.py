import time
from typing import List

from pydantic import BaseModel


class Filament(BaseModel):
    type: str = 'PLA'
    weight: float = 0.75
    price: float = 100
    color: str = 'no color'
    url: str = 'url'
    update_time: int = int(time.time())


class Manufacturer(BaseModel):
    name: str
    filaments: List[Filament] = []


class Manufacturers(BaseModel):
    manufacturers: List[Manufacturer] = []


class Config(BaseModel):
    result_file_path: str
