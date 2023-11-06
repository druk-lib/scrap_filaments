import requests
from bs4 import BeautifulSoup

from schemas import ManufacturerSite, FilamentData

URL = 'https://3dfilament.com.ua'


class ThreeDFilament(FilamentData):
    TYPES = {
        'ABS': 'ABS',
        'PetG': 'PETG',
        'PLA': 'PLA',
    }
    GET_PAGE = True

    def miss(self):
        if 'для 3d ручки' in self.card.find('div', class_='cs-goods-title-wrap').find('a').text:
            return True

        return False

    def get_url(self):
        return f'{URL}{self.card.find("a", class_="cs-goods-title").get("href")}'

    def get_name(self):
        return self.page.find('span', class_='cs-title__product').text

    def get_type(self):
        name = self.get_name()
        for key, value in self.TYPES.items():
            if key in name:
                return value

        return name

    def get_weight(self):
        info_cells = self.page.find_all('td', class_='b-product-info__cell')
        for i, info_cell in enumerate(info_cells):
            if info_cell.text == 'Вага':
                return float(info_cells[i + 1].text.replace('кг', ''))

        name = self.page.find('span', class_='cs-title__product').text
        if 'кг' in name:
            parsed_name = name.split(' ')
            if 'кг' in parsed_name:
                return parsed_name[parsed_name.index('кг') - 1].replace(',', '.')
            for part_name in parsed_name:
                if 'кг' in part_name:
                    return float(part_name.replace('кг', '').replace(',', '.'))

        return 0

    def get_diameter(self):
        info_cells = self.page.find_all('td', class_='b-product-info__cell')
        for i, info_cell in enumerate(info_cells):
            if info_cell.text == 'Діаметр нитки':
                return float(info_cells[i + 1].text.replace('мм', ''))

        return 0

    def get_color(self):
        info_cells = self.page.find_all('td', class_='b-product-info__cell')
        for i, info_cell in enumerate(info_cells):
            if info_cell.text == 'Колір':
                return self.page.find_all("td", class_="b-product-info__cell")[i + 1].text.strip()

        return 'без кольору'

    def get_price(self):
        return float(self.card.find('p', class_='b-product-cost__price').find('span').text.replace('\xa0', ''))


class ThreeDFilamentSite(ManufacturerSite):
    NAME = '3DFilament'
    FILTER = '/ua/product_list?product_items_per_page=48&presence_available=true'
    # FILTER = '/ua/g92198469-petg-copet?product_items_per_page=48'
    # FILTER = '/ua/g90448360-pla-pla-plastik?product_items_per_page=48'
    FILAMENT = ThreeDFilament

    def get_filaments(self):
        response = requests.get(f'{URL}{self.FILTER}', headers=self.HEADERS)

        return (
            BeautifulSoup(response.text, 'lxml').find_all('li', class_='cs-product-gallery__item js-productad')
            if response.status_code == 200
            else []
        )
