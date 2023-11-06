import json

from monofilament import MonofilamentSite
from plexiwire import PlexiwireSite
from pochatok import PochatokSite
from threedfilament import ThreeDFilamentSite
from schemas import Manufacturers

f = open('config.json')

data = json.load(f)

f.close()

if __name__ == '__main__':
    all_mans = [
        # MonofilamentSite,
        PlexiwireSite,
        ThreeDFilamentSite,
        PochatokSite,
    ]
    mans = Manufacturers()

    for man in all_mans:
        mans.manufacturers.append(man().scrap())

    with open(data['result_file_path'], 'w', encoding='utf-8') as f:
        f.write(
            json.dumps(
                [item.model_dump() for item in mans.manufacturers],
                ensure_ascii=False,
                default=str,
                indent=2,
            )
        )
