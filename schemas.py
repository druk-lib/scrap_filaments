import time
from typing import List

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel


class Filament(BaseModel):
    type: str = 'PLA'
    weight: float = 0.75
    price: float = 100
    color: str = 'no color'
    url: str = 'url'
    update_time: int = int(time.time())


class FilamentData:
    HEADERS = {
        'User-Agent': 'Mozilla/5.0',
        'Content-Type': 'text/html',
        'Accept': 'text/html',
    }
    TYPES = {
        'ABS': 'ABS',
        'PetG': 'PETG',
        'PLA': 'PLA',
    }
    GET_PAGE = False

    def __init__(self, card: BeautifulSoup):
        self.card = card
        self.page = self.get_page()

    def get_dict(self):
        return {
            'type': self.get_type(),
            'weight': self.get_weight(),
            'price': self.get_price(),
            'color': self.get_color(),
            'url': self.get_url(),
            'update_time': int(time.time()),
        }

    def get_page(self):
        if self.GET_PAGE:
            return BeautifulSoup(requests.get(self.get_url(), headers=self.HEADERS).text, 'lxml')

        return None

    def miss(self):
        if self.GET_PAGE:
            return False

        return False

    def get_url(self):
        return 'url'

    def get_name(self):
        return ''

    def get_type(self):
        return self.TYPES.get('PLA')

    def get_weight(self):
        return 0.75

    def get_diameter(self):
        return 1.75

    def get_color(self):
        return ''

    def get_price(self):
        return 100


class ManufacturerSite:
    HEADERS = {
        'User-Agent': 'Mozilla/5.0',
        'Content-Type': 'text/html',
        'Accept': 'text/html',
    }
    NAME = 'ManufacturerName'
    URL = 'https://<url>'
    FILTER = '/<filter for available filaments>'
    TYPES = {
        'PLA': 'PLA',
    }
    FILAMENT = FilamentData

    def scrap(self):
        available_filaments = []
        for filament_card in self.get_filaments():
            filament = self.FILAMENT(filament_card)

            if filament.miss():
                continue

            available_filaments.append(Filament(**filament.get_dict()))

        return Manufacturer(name=self.NAME, filaments=available_filaments)

    def get_filaments(self):
        return []


class Manufacturer(BaseModel):
    name: str
    filaments: List[Filament] = []


class Manufacturers(BaseModel):
    manufacturers: List[Manufacturer] = []
