from loguru import logger
from requests import RequestException

from ..schemas import FilamentData, ManufacturerSite, ResponseSoup

URL = 'https://u3df.com.ua'


class U3DF(FilamentData):
    TYPES = {
        'ABS': 'ABS',
        'PETG': 'PETG',
        'CoPET': 'CoPET',
        'PLA': 'PLA',
    }
    GET_PAGE = True

    def miss(self):
        if 'Немає в наявності' in self.card.find('span', class_='cs-goods-data__state').text:
            return True

        return False

    def get_url(self):
        return f'{URL}{self.card.find("a", class_="cs-goods-title").get("href")}'

    def get_name(self):
        return self.card.find('a', class_='cs-goods-title').text

    def get_type(self):
        name = self.get_name()
        for key, value in self.TYPES.items():
            if key in name:
                return value

        return name

    def get_weight(self):
        if product_info := self.page.find('table', class_='b-product-info'):
            for part in product_info.find_all('td', class_='b-product-info__cell'):
                if 'Вага' in part.text:
                    return float(part.find_next('td', class_='b-product-info__cell').text.replace('кг', '').replace(',', '.').strip())
        name_parts = self.get_name().replace('/', ' ').replace(')', ' ').split(' ')
        if 'кг' in name_parts:
            return float(name_parts[name_parts.index('кг') - 1].replace(',', '.'))
        if 'грам' in name_parts:
            return float(name_parts[name_parts.index('грам') - 1].replace(',', '.')) * 0.001 or float(name_parts[name_parts.index('грамм') - 1].replace(',', '.')) * 0.001
        return 0.1

    def get_diameter(self):
        if product_info := self.page.find('table', class_='b-product-info'):
            for part in product_info.find_all('td', class_='b-product-info__cell'):
                if 'Діаметр нитки' in part.text:
                    return float(part.find_next('td', class_='b-product-info__cell').text.replace('мм', '').replace(',', '.').strip())
        return 1.75

    def get_color(self):
        if product_info := self.page.find('table', class_='b-product-info'):
            for part in product_info.find_all('td', class_='b-product-info__cell'):
                if 'Колір' in part.text:
                    return part.find_next('td', class_='b-product-info__cell').text.strip()
        return 'no color'

    def get_price(self):
        return float(
            self.card.find(
                "span",
                class_="cs-goods-price__value",
            )
            .text.replace(u'\xa0', "")
            .replace("₴", "")
        )


class U3DFSite(ManufacturerSite):
    NAME = 'U3DF'
    FILTER = '/ua/g21140449-nit?product_items_per_page=48&availability=availability'
    FILAMENT = U3DF

    def get_filaments(self):
        try:
            bs = ResponseSoup(f'{URL}{self.FILTER}', self.NAME).get_response()
        except RequestException:
            logger.info(f'{self.NAME} - {URL}{self.FILTER} - RequestException')
            return []
        except Exception as e:
            logger.info(f'{self.NAME} - {URL}{self.FILTER} - {e}')
            return []

        return bs.find_all('li', class_='cs-product-gallery__item')
