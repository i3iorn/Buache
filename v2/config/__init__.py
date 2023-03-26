import json
import os
from pathlib import Path
from typing import List

ROOT_PATH = os.getenv('ROOT')

with open(Path(f'{ROOT_PATH}/config/address_components.json').absolute(), 'r') as f:
    ADDRESS_COMPONENT_DEFINITIONS = json.load(f)

ADDRESS_COMPONENT_TYPES = [ad['name'] for ad in ADDRESS_COMPONENT_DEFINITIONS]

with open(Path(f'{ROOT_PATH}/config/countries.json').absolute(), 'r') as f:
    COUNTRY_DEFINITIONS = json.load(f)


class Config:

    @staticmethod
    def countries() -> List[str]:
        return [c['name'] for c in COUNTRY_DEFINITIONS]

    @staticmethod
    def country_codes() -> List[str]:
        return [c['code'] for c in COUNTRY_DEFINITIONS]
