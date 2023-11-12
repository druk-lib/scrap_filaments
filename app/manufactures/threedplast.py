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
        # if 'Немає в наявності' in self.card.find('span', class_='cs-goods-data__state').text:
        #     return True

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
        # TODO from page
        return 0.85

    def get_diameter(self):
        return 1.75

    def get_color(self):
        parsed_name = (
            self.get_name()
            # .replace(",", " ")
            .replace("-", " ")
            .replace("Інженерний ", "")
            .replace("Нитка ", "")
            .replace("Нить ", "")
            .replace("(АБС)", "")
            .replace("пластик для 3D-принтера", "")
            .replace("пластик для 3D принтера", "")
            .replace(" пластик 3Dplast філамент для 3D принтера", "")
            .replace("1.75", "")
            .replace("мм", "")
            .replace("кг.", "")
            .replace("кг", "")
            .replace("   ", " ")
            .replace("  ", " ")
            .replace(",,", "")
            .replace(", ", "")
            .strip()
            .split(" ")
        )
        print(self.get_name())
        print(parsed_name)
        return parsed_name[-1]

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
        bs = ResponseSoup(f"{URL}{self.FILTER}", self.NAME).get_response()

        return bs.find_all("li", class_="cs-product-gallery__item")
