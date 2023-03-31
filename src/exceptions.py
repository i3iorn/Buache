class BuacheException(Exception):
    pass


class ConfigurationError(BuacheException):
    pass


class AddressException(BuacheException):
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


class AddressException(BuacheException):
    pass


class AddressComponentException(AddressException):
    pass


class AddressComponentNotFound(AddressComponentException):
    pass


class ComponentThresholdNotReached(AddressComponentException):
    pass


class EmptyListException(BuacheException):
    pass


class RuleException(BuacheException):
    pass


class ConditionalException(RuleException):
    pass


class CriteriaTypeError(RuleException):
    pass


class EvaluationException(RuleException):
    pass


class MissingCriteriaError(RuleException):
    pass


class MissingConstantError(RuleException):
    pass


class FailedToSaveRuleException(RuleException):
    pass


class InvalidOperatorError(ConditionalException):
    pass


class MissingRuleDeclarationForComponent(RuleException):
    pass


class ToManyRulesDeclaredForComponent(RuleException):
    pass


class AmbiguousScoresException(AddressException):
    pass
