import requests
from bs4 import BeautifulSoup

from schemas import FilamentData, ManufacturerSite

URL = 'https://shop.plexiwire.com.ua'


class Plexiwire(FilamentData):
    TYPES = {
        'ABS': 'ABS',
        'PETG': 'PETG',
        'PLA': 'PLA',
    }
    GET_PAGE = False

    def get_url(self):
        return self.card.find('a').get('href')

    def get_name(self):
        return self.card.find('div', class_='catalogCard-title').find('a').get('title')

    def get_type(self):
        type_site = self.get_name().split(' ')[0]
        return self.TYPES.get(type_site) or type_site

    def get_weight(self):
        return float(self.get_name().split(' ')[-3].replace('кг', ''))

    def get_diameter(self):
        return float(self.get_name().split(' ')[1].replace('мм', ''))

    def get_color(self):
        return self.get_name().split(' ')[-6]

    def get_price(self):
        return float(self.card.find('div', class_='catalogCard-price').text.strip().split(' ')[0])


class PlexiwireSite(ManufacturerSite):
    NAME = 'Plexiwire'
    FILTER = '/plexiwire-filament/filter/presence=1/'
    FILAMENT = Plexiwire

    def get_filaments(self):
        response = requests.get(f'{URL}{self.FILTER}', headers=self.HEADERS)

        return BeautifulSoup(response.text, 'lxml').find_all('li', class_='catalog-grid__item') if response.status_code == 200 else []
