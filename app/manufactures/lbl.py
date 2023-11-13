from loguru import logger
from requests import RequestException

from ..schemas import FilamentData, ManufacturerSite, ResponseSoup

URL = 'https://lbl-corp.com'


class LBL(FilamentData):
    TYPES = {
        'ABS': 'ABS',
        'CoPET': 'CoPET',
        'PLA': 'PLA',
    }
    GET_PAGE = True

    def miss(self):
        if '3D принтера' in self.get_name():
            return False

        return True

    def get_url(self):
        return f'{URL}{self.card.find("a", class_="b-goods-title").get("href")}'

    def get_name(self):
        return self.card.find('a', class_='b-product-gallery__title').text

    def get_type(self):
        type_site = self.get_name().split(' ')[0]
        return self.TYPES.get(type_site) or type_site

    def get_weight(self):
        split_name = self.get_name().split(' ')
        return float(split_name[split_name.index('кг') - 1])

    def get_diameter(self):
        split_name = self.get_name().split(' ')
        return float(split_name[split_name.index('мм') - 1])

    def get_color(self):
        split_name = self.get_name().split(' ')
        return ' '.join(split_name[split_name.index('мм') + 2 :])

    def get_price(self):
        return float(
            self.card.find('span', class_='b-goods-price__value b-goods-price__value_type_current')
            .text.replace('\xa0', '')
            .replace('₴', '')
        )


class LBLSite(ManufacturerSite):
    NAME = 'LBL'
    FILTER = '/ua/product_list?product_items_per_page=48&presence_available=true&bss0=296795'
    FILAMENT = LBL

    def get_filaments(self):
        try:
            bs = ResponseSoup(f'{URL}{self.FILTER}', self.NAME).get_response()
        except RequestException:
            logger.info(f'{self.NAME} - {URL}{self.FILTER} - RequestException')
            return []
        except Exception as e:
            logger.info(f'{self.NAME} - {URL}{self.FILTER} - {e}')
            return []

        return bs.find_all('li', class_='b-product-gallery__item')
