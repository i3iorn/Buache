import configparser
import logging
import os
from pathlib import Path
from typing import TYPE_CHECKING

import langdetect

import config
from config import CONFIG
from .component import AddressComponentType
from .parser import AddressParser
from .ml_parser import MLAddressParser

__all__ = [
    'AddressParser',
    'MLAddressParser',
    'Address'
]

if TYPE_CHECKING:
    from .. import Application


class Address:
    def __init__(self,
                 app: 'Application',
                 address_string: str = None,
                 use_ml: bool = False
                 ):
        self.log = logging.getLogger(__name__)
        self.app = app

        self.country_code = self.detect_language(address_string)
        self.log.debug(f'Country code "{self.country_code}" was detected from the input_address.')

        self.load_country_config()

        if use_ml:
            self.log.info(f'Using machine learning when parsing address.')
            self.parser = MLAddressParser()
        else:
            self.log.info(f'Using heuristics when parsing address.')
            self.parser = AddressParser()

        if address_string is not None:
            self.log.debug(f'Starting {__name__} with address_string = {address_string.__str__()}')
            self.components = self.parser.parse_address(address_string)

    @property
    def full_address(self) -> str:
        try:
            fmt = CONFIG.get('Address', 'FORMAT')
            components = {c.component_type.name.lower(): c.component_value for c in self.components}
            self.log.debugx(fmt)
            self.log.debugx(components)
            fa = str(fmt).format(**components)
        except configparser.NoSectionError as e:
            self.log.warning(f'Returning all components as no format is specified for this country. ')
            fa = " ".join([c.component_value for c in self.components])

        return fa

    def detect_language(self, input_address: str) -> str:
        """
        Detect the language of the input address using language detection techniques.
        """
        return langdetect.detect(input_address)

    def load_country_config(self):
        CONFIG.read(Path(f"{config.country_folder}/default.ini").absolute())
        country_config_folder = Path(f"{config.country_folder}/{self.country_code}")
        if country_config_folder.exists():
            for config_file in country_config_folder.iterdir():
                CONFIG.read(config_file)
        else:
            self.log.warning(f'Failed to load config for {self.country_code}\n'
                             f'{country_config_folder}')

        self.log.debug(f'Configuration for "{self.country_code}" is loaded.')

        self.log.debugx(f'Update AddressComponentType order based on configuration.')
        for ac_type, position in CONFIG.items('AddressComponentType'):
            self.log.trace(f'{ac_type}: {position}')
            AddressComponentType[ac_type.upper()].__init__(position)
