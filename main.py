import json

from monofilament import MonofilamentSite
from plexiwire import PlexiwireSite
from schemas import Manufacturers

if __name__ == '__main__':
    all_mans = [
        MonofilamentSite,
        PlexiwireSite,
    ]
    mans = Manufacturers()

    for man in all_mans:
        mans.manufacturers.append(man().scrap())

    with open('data.json', 'w', encoding='utf-8') as f:
        f.write(
            json.dumps(
                [item.model_dump() for item in mans.manufacturers],
                ensure_ascii=False,
                indent=2,
            )
        )
