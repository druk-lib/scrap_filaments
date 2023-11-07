import requests
from bs4 import BeautifulSoup

from ..schemas import FilamentData, ManufacturerSite


class MonofilamentSite:
    HEADERS = {
        'User-Agent': 'Mozilla/5.0',
        'Content-Type': 'text/html',
        'Accept': 'text/html',
    }
    NAME = 'MonoFilament'
    URL = 'https://shop.plexiwire.com.ua'
    FILTER = '/plexiwire-filament/filter/presence=1/'
    TYPES = {
        'ABS': 'ABS',
        'coPET': 'CoPET',
        'PLA': 'PLA',
    }

    @staticmethod
    def get_pages():
        return [
            {
                'url': 'https://monofilament.com.ua/ua/products/standartnye-materialy/abs/',
                'filter': '?ocf=F3S0V2F3S3V19&limit=100',
            },
            {
                'url': 'https://monofilament.com.ua/ua/products/standartnye-materialy/copet/',
                'filter': '?ocf=F3S0V2F3S3V19&limit=100',
            },
        ]

    def scrap(self):
        available_filaments = []
        for page in self.get_pages():
            for filament in self.get_filaments(f'{page["url"]}{page["filter"]}'):
                buttons = filament.find('div', class_='hpm-button-wrapper').find_all('button', class_='hpm-button')

                for button in buttons:
                    if 'out-stock' in button.get('class'):
                        continue

                    if '1,75' not in button.text:
                        continue

                    href = self.get_href(filament)
                    filament_card = self.get_filament_card(href)
                    name = self.get_name(filament_card)
                    color = self.get_color(filament_card, page['type_in_name'])
                    price = self.get_price(filament_card)

                    available_filaments.append(
                        Filament(
                            name=name,
                            type=page['type_for_site'],
                            weight=self.get_weight(button),
                            price=price,
                            color=color,
                            url=href,
                        )
                    )
        return Manufacturer(name='Monofilament', filaments=available_filaments)

    def get_filaments(self, url_filter: str):
        response = requests.get(url_filter, headers=self.HEADERS)

        return BeautifulSoup(response.text, 'lxml').find_all('div', class_='product-thumb') if response.status_code == 200 else []

    def get_filament_card(self, url: str):
        response = requests.get(url, headers=self.HEADERS)
        return BeautifulSoup(response.text, 'lxml')

    @staticmethod
    def get_name(filament_card):
        return filament_card.find('h1').text or filament_card.find('h4').text

    @staticmethod
    def get_weight(button):
        return float(button.text[button.text.find('Вага:') + 5 :].replace('кг', '').replace(',', '.'))

    @staticmethod
    def get_diameter(button):
        return float(button.text[1 : button.text.find('мм')].replace(',', '.'))

    def get_color(self, filament, type_in_name):
        return self.get_name(filament).text.replace(type_in_name, '').strip()

    @staticmethod
    def get_href(filament):
        return filament.find('h4').find('a').get('href')

    @staticmethod
    def get_price(filament):
        formated_price = filament.find('span', id='formated_price')

        return formated_price and int(float(formated_price.get('price'))) or 0
