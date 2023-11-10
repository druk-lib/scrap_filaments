import json
import os
import random
import time

import requests
from bs4 import BeautifulSoup

from ..utils import settings

HEADERS = {
    'User-Agent': 'Mozilla/5.0',
    'Content-Type': 'text/html',
    'Accept': 'text/html',
}


class ResponseSoup:
    def __init__(self, url: str, file_name: str):
        self.url = url
        self.file_name = f'{settings.path_debug_data}{file_name.replace("/", "_").replace("?", "_")}.html'

    def get_response(self):
        if settings.debug and os.path.exists(self.file_name):
            with open(self.file_name) as f:
                return BeautifulSoup(f.read(), 'lxml')

        time.sleep(random.randrange(1, 4))
        response = requests.get(self.url, headers=HEADERS)
        if settings.debug:
            with open(self.file_name, 'w') as f:
                f.write(response.text)

        return BeautifulSoup(response.text, 'lxml')


class ResponseJSON:
    def __init__(self, url: str, file_name: str):
        self.url = url
        self.file_name = f'{settings.path_debug_data}{file_name.replace("/", "_")}.json'

    def get_response(self):
        if settings.debug and os.path.exists(self.file_name):
            with open(self.file_name) as f:
                return json.load(f)

        response = requests.get(self.url, headers=HEADERS)
        if settings.debug:
            with open(self.file_name, 'w') as f:
                f.write(
                    json.dumps(
                        response.json(),
                        ensure_ascii=False,
                        default=str,
                        indent=2,
                    )
                )

        return response.json()
