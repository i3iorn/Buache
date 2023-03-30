import logging

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
        if use_ml:
            self.log.info(f'Using machine learning when parsing address.')
            self.parser = MLAddressParser()
        else:
            self.log.info(f'Using heuristics when parsing address.')
            self.parser = AddressParser()

        if address_string is not None:
            self.log.debug(f'Starting {__name__} with address_string = {address_string.__str__()}')
            self.components = self.parser.parse_address(address_string)
