from loguru import logger

from .filament import FilamentData
from .schemas import Filament, Manufacturer


class ManufacturerSite:
    HEADERS = {
        'User-Agent': 'Mozilla/5.0',
        'Content-Type': 'text/html',
        'Accept': 'text/html',
    }
    NAME = 'ManufacturerName'
    URL = 'https://<url>'
    FILTER = '/<filter for available filaments>'
    TYPES = {
        'PLA': 'PLA',
    }
    FILAMENT = FilamentData

    def scrap(self):
        available_filaments = []
        for filament_card in self.get_filaments():
            filament = self.FILAMENT(filament_card)

            try:
                if filament.miss():
                    continue

                available_filaments.append(Filament(**filament.get_dict()))

            except Exception as e:
                logger.info(f'{self.NAME} - {e} - {filament.get_url()}')
                continue

        return Manufacturer(name=self.NAME, filaments=available_filaments)

    def get_filaments(self):
        return []
