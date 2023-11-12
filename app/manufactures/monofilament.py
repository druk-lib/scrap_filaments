import random
import time

from loguru import logger
from requests import RequestException

from ..schemas import FilamentData, ManufacturerSite, ResponseJSON, ResponseSoup

URL = 'https://monofilament.com.ua'


class Monofilament(FilamentData):
    TYPES = {
        'ABS': 'ABS',
        'coPET': 'CoPET',
        'PLA': 'PLA',
    }
    GET_PAGE = True

    def get_page(self):
        if self.GET_PAGE:
            time.sleep(random.randrange(1, 4))

            return ResponseJSON(
                f'{URL}/index.php?route=module/hpmrr/product_json&pid={self.card}',
                self.card,
            ).get_response()['success']

        return None

    def miss(self):
        return '2,90' in self.page['name']

    def get_url(self):
        return self.page['href']

    def get_name(self):
        return self.page['name']

    def get_type(self):
        type_site = self.get_name().split(' ')[0]
        return self.TYPES.get(type_site) or type_site

    def get_weight(self):
        # TODO regexp
        return float(self.get_name().split(' ')[-1].replace('кг', '').replace('Вес:', '').replace(',', '.'))

    def get_diameter(self):
        name = self.get_name().split(' ')
        return float(name[name.index('мм') - 1].replace('Ø', '').replace(',', '.'))

    def get_color(self):
        return self.get_name().split(' ')[1]

    def get_price(self):
        return float(self.page['price_noformat'])


class MonofilamentSite(ManufacturerSite):
    NAME = 'MonoFilament'
    FILTERS = (
        '/ua/products/standartnye-materialy/abs/?ocf=F3S0V2F3S3V19&limit=100',
        '/ua/products/standartnye-materialy/copet/?ocf=F3S0V2F3S3V19&limit=100',
        '/ua/products/standartnye-materialy/pla/?ocf=F3S0V2F3S3V19&limit=100',
        '/ua/products/standartnye-materialy/pla-plus/?ocf=F3S0V2F3S3V19&limit=100',
    )
    FILAMENT = Monofilament

    def get_filaments(self):
        page_ids = []
        for filter_url in self.FILTERS:
            try:
                bs = ResponseSoup(f'{URL}{filter_url}', filter_url.split('/')[-2]).get_response()
            except RequestException:
                logger.info(f'{self.NAME} - {URL}{filter_url} - RequestException')
                continue

            for card in bs.find_all('div', class_='product-thumb'):
                buttons = card.find('div', class_='custom1').find_all('button', class_='hpm-button')
                for button in buttons:
                    if 'out-stock' in button.get('class'):
                        continue
                    page_ids += button.get('data-ids').split(',')

        return set(page_ids)
