class AddressException(Exception):
    pass


class AddressTokenizationException(AddressException):
    pass


class MissingAddressComponentEvaluation(AddressException):
    pass


class ComponentException(AddressException):
    pass


class ComponentEvaluationException(ComponentException):
    pass


class InconclusiveEvaluationException(ComponentEvaluationException):
    pass
