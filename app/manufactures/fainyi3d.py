from ..schemas import FilamentData, ManufacturerSite, ResponseSoup

URL = 'https://fainyi3d.com'


class Fainyi3D(FilamentData):
    TYPES = {
        'ABS': 'ABS',
        'PETG': 'PETG',
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
        parsed_name = self.get_name().split(' ')
        return float(parsed_name[parsed_name.index('кг') - 1])

    def get_diameter(self):
        parsed_name = self.get_name().split(' ')
        return float(parsed_name[parsed_name.index('мм') - 1])

    def get_color(self):
        parsed_name = self.get_name().split(' ')
        return parsed_name[-1]

    def get_price(self):
        return float(self.card.find('span', class_='cs-goods-price__value cs-goods-price__value_type_current').text.replace('₴', ''))


class Fainyi3DSite(ManufacturerSite):
    NAME = 'ФАЙНИЙ'
    FILTER = '/ua/product_list?presence_available=true'
    FILAMENT = Fainyi3D

    def get_filaments(self):
        bs = ResponseSoup(f'{URL}{self.FILTER}', self.NAME).get_response()

        return bs.find_all('li', class_='cs-product-gallery__item js-productad')
