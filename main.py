import json

from loguru import logger

from app.manufactures import MonofilamentSite, PlexiwireSite, PochatokSite, ThreeDFilamentSite, BozeSite, LBLSite
from app.schemas.schemas import Manufacturers
from app.utils import settings

if __name__ == '__main__':
    all_mans = [
        MonofilamentSite,
        # PlexiwireSite,
        # ThreeDFilamentSite,
        # PochatokSite,
        # BozeSite,
        # LBLSite,
    ]
    mans = Manufacturers()

    for man in all_mans:
        logger.info(f'Scrapping {man.NAME}')

        mans.manufacturers.append(man().scrap())

    with open(settings.result_file_path, 'w', encoding='utf-8') as f:
        f.write(
            json.dumps(
                [item.model_dump() for item in mans.manufacturers],
                ensure_ascii=False,
                default=str,
                indent=2,
            )
        )
        logger.info(f'Saved to {settings.result_file_path}')
