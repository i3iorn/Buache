class ApplicationError(Exception):
    pass


class ConfigurationError(ApplicationError):
    pass


class AddressException(ApplicationError):
    pass


class NormalizationError(AddressException):
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
