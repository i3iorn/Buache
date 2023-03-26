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


class EmptyListException(BuacheException):
    pass


class RuleException(BuacheException):
    pass


class ConditionalException(RuleException):
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