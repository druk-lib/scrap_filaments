from datetime import datetime

import requests
from bs4 import BeautifulSoup

from schemas import Filament, Manufacturer


class PlexiwireSite:
    HEADERS = {
        'User-Agent': 'Mozilla/5.0',
        'Content-Type': 'text/html',
        'Accept': 'text/html',
    }
    NAME = 'Plexiwire'
    URL = 'https://shop.plexiwire.com.ua'
    FILTER = '/plexiwire-filament/filter/presence=1/'
    TYPES = {
        'ABS': 'ABS',
        'PETG': 'PETG',
        'PLA': 'PLA',
    }

    def scrap(self):
        available_filaments = []
        for filament in self.get_filaments(f'{self.URL}{self.FILTER}'):
            if created_filament := self.create_filament(filament):
                available_filaments.append(created_filament)

        return Manufacturer(name=self.NAME, filaments=available_filaments)

    def create_filament(self, filament):
        title = filament.find('div', class_='catalogCard-title').find('a').get('title').split(' ')

        return Filament(
            name=self.get_name(title),
            type=self.get_type(title),
            weight=self.get_weight(title),
            price=self.get_price(filament),
            color=self.get_color(title),
            url=f'{self.URL}{self.get_href(filament)}',
            update_time=datetime.now(),
        )

    def get_filaments(self, url_filter: str):
        response = requests.get(url_filter, headers=self.HEADERS)

        return BeautifulSoup(response.text, 'lxml').find_all('li', class_='catalog-grid__item') if response.status_code == 200 else []

    @staticmethod
    def get_name(title):
        return ' '.join(title)

    def get_type(self, title):
        return self.TYPES.get(title[0]) or title[0]

    @staticmethod
    def get_weight(title):
        return float(title[-3].replace('кг', ''))

    @staticmethod
    def get_diameter(filament):
        return float(filament.find('a').get('title').split(' ')[1].replace('мм', ''))

    @staticmethod
    def get_color(title):
        return title[-6]

    @staticmethod
    def get_href(filament):
        return filament.find('a').get('href')

    @staticmethod
    def get_price(filament):
        return float(filament.find('div', class_='catalogCard-price').string.strip().split(' ')[0])
