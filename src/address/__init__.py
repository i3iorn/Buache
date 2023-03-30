import configparser
import logging
import os
from pathlib import Path

import langdetect

from .parser import AddressParser
from .ml_parser import MLAddressParser

__all__ = [
    'AddressParser',
    'MLAddressParser',
    'Address'
]


class Address:
    def __init__(self,
                 address_string: str = None,
                 use_ml: bool = False
                 ):
        self.log = logging.getLogger(__name__)

        self.country_code = self.detect_language(address_string)
        self.log.debug(f'Country code "{self.country_code}" was detected from the input_address.')

        self.country = self.load_country_config()

        if use_ml:
            self.log.info(f'Using machine learning when parsing address.')
            self.parser = MLAddressParser()
        else:
            self.log.info(f'Using heuristics when parsing address.')
            self.parser = AddressParser(self.country)

        if address_string is not None:
            self.log.debug(f'Starting {__name__} with address_string = {address_string.__str__()}')
            self.components = self.parser.parse_address(address_string)
            self.components.sort()

    @property
    def full_address(self) -> str:
        return self._components

    def detect_language(self, input_address: str) -> str:
        """
        Detect the language of the input address using language detection techniques.
        """
        return langdetect.detect(input_address)

    def load_country_config(self):
        country_config_file = Path(f"{os.getenv('ROOT')}/config/countries/{self.country_code}.ini")
        if not country_config_file.exists():
            self.log.info(f'No country information is configured. Using default values.')
            country_config_file = Path(f"{os.getenv('ROOT')}/config/countries/default.ini")

        country = configparser.ConfigParser()
        country.read(country_config_file.absolute())
        self.log.debug(country.sections())
        self.log.debug(f'Configuration for "{self.country_code}" is loaded.')
        return country
