class BuacheException(Exception):
    pass


class AddressException(BuacheException):
    pass


class AddressComponentException(AddressException):
    pass


class AddressComponentNotFound(AddressComponentException):
    pass


class ComponentThresholdNotReached(AddressComponentException):
    pass
