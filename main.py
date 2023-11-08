import json
import os

from app.manufactures import PlexiwireSite, PochatokSite, ThreeDFilamentSite
from app.schemas.schemas import Manufacturers, Config


if __name__ == '__main__':
    with open(os.getcwd() + '/config.json') as f:
        config = Config(**json.load(f))

    all_mans = [
        # MonofilamentSite,
        PlexiwireSite,
        ThreeDFilamentSite,
        PochatokSite,
    ]
    mans = Manufacturers()

    for man in all_mans:
        mans.manufacturers.append(man().scrap())

    with open(config.result_file_path, 'w', encoding='utf-8') as f:
        f.write(
            json.dumps(
                [item.model_dump() for item in mans.manufacturers],
                ensure_ascii=False,
                default=str,
                indent=2,
            )
        )
