from loguru import logger
from requests import RequestException

from ..schemas import FilamentData, ManufacturerSite, ResponseSoup

URL = "https://3dplast.biz"


class ThreeDPlast(FilamentData):
    TYPES = {
        "ABS": "ABS",
        "PETg": "PETG",
        "CoPET": "CoPET",
        "PLA": "PLA",
    }
    GET_PAGE = True

    def miss(self):
        if 'Немає в наявності' in self.card.find('span', class_='cs-goods-data__state').text:
            return True

        return False

    def get_url(self):
        return f'{URL}{self.card.find("a", class_="cs-goods-title").get("href")}'

    def get_name(self):
        return self.card.find("a", class_="cs-goods-title").text

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
        return 0.85

    def get_diameter(self):
        return 1.75

    def get_color(self):
        if product_info := self.page.find('table', class_='b-product-info'):
            for part in product_info.find_all('td', class_='b-product-info__cell'):
                if 'Колір' in part.text:
                    return part.find_next('td', class_='b-product-info__cell').text
        return 'no color'

    def get_price(self):
        return float(
            self.card.find(
                "span",
                class_="cs-goods-price__value cs-goods-price__value_type_current",
            )
            .text.replace(u'\xa0', "")
            .replace("₴", "")
        )


class ThreeDPlastSite(ManufacturerSite):
    NAME = "3dplast"
    FILTER = "/ua/g97296511-plastik-diametr-175"
    FILAMENT = ThreeDPlast

    def get_filaments(self):
        try:
            bs = ResponseSoup(f'{URL}{self.FILTER}', self.NAME).get_response()
        except RequestException:
            logger.info(f'{self.NAME} - {URL}{self.FILTER} - RequestException')
            return []

        return bs.find_all("li", class_="cs-product-gallery__item")
