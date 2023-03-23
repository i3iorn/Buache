import json
import logging.config
from pathlib import Path

from .address import Address
from .address_component import AddressComponent
from .adapter import Adapter, AuthenticatedAPIAdapter, UnauthenticatedAPIAdapter, \
                     FileAdapter, FTPAdapter, HTTPAdapter, LocalAdapter
from .augmentor import Augmentor
from .source import Source
from .rule import Rule

__all__ = [
    'Address',
    'Adapter',
    'AuthenticatedAPIAdapter',
    'UnauthenticatedAPIAdapter',
    'FileAdapter',
    'FTPAdapter',
    'HTTPAdapter',
    'LocalAdapter',
    'Augmentor',
    'Source',
    'Rule',
    'AddressComponent'
]

# Define custom logging levels
new_levels = {
    'VERBOSE': 15,
    'TRACE': 5
}

for name, level in new_levels.items():
    logging.addLevelName(level, name.upper())
    logging.addLevelName(level, name.lower())

    def function(self, message, *args, **kwargs):
        if self.isEnabledFor(level):
            self._log(level, message, args, **kwargs)

    setattr(logging.Logger, name.lower(), function)

with open(Path('config/log.config').absolute(), 'r') as log_config:
    logging.config.dictConfig(json.load(log_config))
