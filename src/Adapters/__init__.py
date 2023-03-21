import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.address import Address


class BaseAdapter:
    def __init__(self, config):
        self.log = logging.getLogger(config['name'])
        self.pre_load = (config['type'] != 'api')
        self.name = config['name']

    def get_new_data(self, address: 'Address') -> bool:
        raise NotImplementedError

    def status(self) -> bool:
        raise NotImplementedError

    def validate_address(self, address: 'Address') -> bool:
        raise NotImplementedError
