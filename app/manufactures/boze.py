from ..schemas import FilamentData, ManufacturerSite, ResponseSoup

URL = 'https://www.boze.com.ua'


class Boze(FilamentData):
    TYPES = {
        'ABS': 'ABS',
        'PETG': 'PETG',
        'PLA': 'PLA',
    }
    GET_PAGE = True

    def miss(self):
        if self.GET_PAGE:
            return False

        return False

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
                if 'Вес' in part.text:
                    return float(part.text.split(' ')[1].replace('KG', ''))
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
    FILTERS = (
        '/index.php/ru/shop/pla?limit=100',
        '/index.php/ru/shop/pla-metalik?limit=100',
        '/index.php/ru/shop/abs-boze?limit=100',
    )
    FILTER = '/index.php/ru/shop'
    FILAMENT = Boze

    def get_filaments(self):
        cards = []
        for filter_url in self.FILTERS:
            bs = ResponseSoup(f'{URL}{filter_url}', filter_url.split('/')[-1]).get_response()

            cards += bs.find_all('div', class_='product-box')

        return cards
