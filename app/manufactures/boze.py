from ..schemas import FilamentData, ManufacturerSite
from ..schemas.response_soup import ResponseSoup

URL = 'https://www.boze.com.ua'


class Boze(FilamentData):
    TYPES = {
        'ABS': 'ABS',
        'PETG': 'PETG',
        'PLA': 'PLA',
    }
    GET_PAGE = True

    def get_url(self):
        return f'{URL}{self.card.find("a").get("href")}'

    def get_name(self):
        return self.card.find('div', class_='Title').find('a').get('title')

    def get_type(self):
        type_site = self.get_name().split(' ')[0]
        return self.TYPES.get(type_site) or type_site

    def get_weight(self):
        if dimensions := self.page.find('div', class_='Dimensions'):
            for part in dimensions.find_all('div'):
                if 'Вес' in part:
                    return float(part.split(' ')[1].replace('KG', ''))
        return 0

    def get_diameter(self):
        short_desc = self.page.final('dev', class_='short_desc')
        if short_desc and 'mm' in short_desc.text:
            short_desc = short_desc.text.split(' ')
            for part in short_desc:
                if 'mm' in part:
                    return float(part.replace('mm', ''))

        return 1.75

    def get_color(self):
        return ' '.join(self.get_name().split(' ')[1:])

    def get_price(self):
        return float(self.card.find('span', class_='sales').text.replace(',', '.').split(' ')[0])


class BozeSite(ManufacturerSite):
    NAME = 'BOZE'
    FILTER = '/index.php/ru/shop'
    FILAMENT = Boze

    def get_filaments(self):
        bs = ResponseSoup(f'{URL}{self.FILTER}', self.NAME).get_response()

        return bs.find_all('div', class_='product-box')
