from loguru import logger
from requests import RequestException

from ..schemas import FilamentData, ManufacturerSite, ResponseSoup

URL = 'https://pochatok-filament.uaprom.net'


class Pochatok(FilamentData):
    TYPES = {
        'ABS': 'ABS',
        'PetG': 'PETG',
        'PLA': 'PLA',
    }

    def miss(self):
        if self.card.find('span', class_='cs-goods-data__state').text == 'Немає в наявності':
            return True
        if 'Набір' in self.get_name():
            return True

        return False

    def get_url(self):
        return f'{URL}{self.card.find("a", class_="cs-goods-title").get("href")}'

    def get_name(self):
        return self.card.find('a', class_='cs-goods-title').text

    def get_type(self):
        return self.TYPES.get('PLA')

    def get_weight(self):
        return 0.75

    def get_diameter(self):
        return 1.75

    def get_color(self):
        return (
            self.get_name()
            .replace('PLA філамент нитка пластик для 3D друку Pochatok Filament 1,75 мм', '')
            .replace('PLA філамент нитка пластик для ЗD друку Pochatok Filament 1,75 мм', '')
            .replace('.', '')
            .strip()
        )

    def get_price(self):
        return float(
            self.card.find('span', class_='cs-goods-price__value cs-goods-price__value_type_current')
            .text.replace('\xa0', '')
            .replace('₴', '')
        )


class PochatokSite(ManufacturerSite):
    NAME = 'Pochatok filament'
    FILTER = '/ua/g94039223-plastik-dlya-printera?product_items_per_page=48'
    FILAMENT = Pochatok

    def get_filaments(self):
        try:
            bs = ResponseSoup(f'{URL}{self.FILTER}', self.NAME).get_response()
        except RequestException:
            logger.info(f'{self.NAME} - {URL}{self.FILTER} - RequestException')
            return []

        return bs.find_all('li', class_='cs-product-gallery__item js-productad')
