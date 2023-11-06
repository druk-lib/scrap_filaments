from datetime import datetime

import requests
from bs4 import BeautifulSoup

from schemas import Filament, Manufacturer


class ThreeDFilamentSite:
    HEADERS = {
        'User-Agent': 'Mozilla/5.0',
        'Content-Type': 'text/html',
        'Accept': 'text/html',
    }
    NAME = '3DFilament'
    URL = 'https://3dfilament.com.ua'
    FILTER = '/ua/product_list?product_items_per_page=48&presence_available=true'
    # FILTER = '/ua/g92198469-petg-copet?product_items_per_page=48'
    # FILTER = '/ua/g90448360-pla-pla-plastik?product_items_per_page=48'
    TYPES = {
        'ABS': 'ABS',
        'PetG': 'PETG',
        'PLA': 'PLA',
    }

    def scrap(self):
        available_filaments = []
        for filament in self.get_filaments(f'{self.URL}{self.FILTER}'):
            if created_filament := self.create_filament(filament):
                available_filaments.append(created_filament)

        return Manufacturer(name=self.NAME, filaments=available_filaments)

    def create_filament(self, filament):
        # if filament.find('span', class_='cs-goods-data__state').text != 'В наявності':
        #     return False
        if 'для 3d ручки' in filament.find('div', class_='cs-goods-title-wrap').find('a').text:
            return False

        href = self.get_href(filament)
        filament_card = self.get_filament_card(href)
        name = self.get_name(filament_card)

        return Filament(
            name=name,
            type=self.get_type(name),
            weight=self.get_weight(filament_card),
            price=self.get_price(filament_card),
            color=self.get_color(filament_card),
            url=href,
            update_time=datetime.now(),
        )

    def get_filaments(self, url_filter: str):
        response = requests.get(url_filter, headers=self.HEADERS)

        return (
            BeautifulSoup(response.text, 'lxml').find_all('li', class_='cs-product-gallery__item js-productad')
            if response.status_code == 200
            else []
        )

    def get_filament_card(self, url: str):
        response = requests.get(url, headers=self.HEADERS)
        return BeautifulSoup(response.text, 'lxml')

    @staticmethod
    def get_name(filament_card):
        return filament_card.find('span', class_='cs-title__product').text

    def get_type(self, name):
        for key, value in self.TYPES.items():
            if key in name:
                return value
        return name

    @staticmethod
    def get_weight(filament_card):
        info_cells = filament_card.find_all('td', class_='b-product-info__cell')
        for i, info_cell in enumerate(info_cells):
            if info_cell.text == 'Вага':
                return float(info_cells[i + 1].text.replace('кг', ''))

        name = filament_card.find('span', class_='cs-title__product').text
        if 'кг' in name:
            parsed_name = name.split(' ')
            if 'кг' in parsed_name:
                return parsed_name[parsed_name.index('кг') - 1].replace(',', '.')
            for part_name in parsed_name:
                if 'кг' in part_name:
                    return float(part_name.replace('кг', '').replace(',', '.'))

        return 0

    @staticmethod
    def get_diameter(filament_card):
        info_cells = filament_card.find_all('td', class_='b-product-info__cell')
        for i, info_cell in enumerate(info_cells):
            if info_cell.text == 'Діаметр нитки':
                return float(info_cells[i + 1].text.replace('мм', ''))
        return 0

    @staticmethod
    def get_color(filament_card):
        info_cells = filament_card.find_all('td', class_='b-product-info__cell')
        for i, info_cell in enumerate(info_cells):
            if info_cell.text == 'Колір':
                return filament_card.find_all("td", class_="b-product-info__cell")[i + 1].text.strip()
        return 'без кольору'

    def get_href(self, filament):
        return f'{self.URL}{filament.find("a", class_="cs-goods-title").get("href")}'

    @staticmethod
    def get_price(filament_card):
        return float(filament_card.find('p', class_='b-product-cost__price').find('span').text.replace('\xa0', ''))
