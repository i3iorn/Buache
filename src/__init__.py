import logging
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
logging.VERBOSE = 15
logging.TRACE = 5


# Define trace and verbose methods on Logger class
def logger_trace(self, message, *args, **kwargs):
    if self.isEnabledFor(logging.TRACE):
        self._log(logging.TRACE, message, args, **kwargs)


def logger_verbose(self, message, *args, **kwargs):
    if self.isEnabledFor(logging.VERBOSE):
        self._log(logging.VERBOSE, message, args, **kwargs)


logging.Logger.trace = logger_trace
logging.Logger.verbose = logger_verbose
