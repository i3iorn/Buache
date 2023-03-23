class BuacheException(Exception):
    pass


class AddressException(BuacheException):
    pass


class ComponentException(AddressException):
    pass


class ComponentNotFound(ComponentException):
    pass
