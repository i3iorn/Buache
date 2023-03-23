import logging
import operator
from typing import List

from src import AddressComponent
from src.exceptions import InvalidOperatorError, MissingCriteriaError, MissingConstantError


class Rule:
    OPERATORS = {
        '<': operator.lt,
        '>': operator.gt,
        '==': operator.is_
    }

    """
    A class to define a parsing rule.
    """
    def __init__(
            self,
            name: str,
            criteria: List[dict]
    ) -> None:
        """
        Constructor method.
        :param name: the name of the parsed address part
        :param criteria: Criteria declaration
        dictated by the criteria_type.
        """
        self.log = logging.getLogger(__name__)
        self.name: str = name
        self.criteria: List[dict] = criteria

    def evaluate(self, index: int, address_substring: str, components: List[AddressComponent]):
        """
        Checks if the rule matches the address.
        :param index: start position in full string.
        :param address_substring: Part of address.
        :param components: a list containing previously identified address components
        :return: True if the rule matches, False otherwise
        """
        try:
            for crit in self.criteria:
                operation_type, op, val2 = crit.values()
                func_ = self.OPERATORS[op]

                if operation_type in ['index', 'compare']:
                    val2 = self.value(val2, components)
                    if val2 is not None:
                        if operation_type == 'index':
                            val1 = index
                        else:
                            val1 = address_substring

                        if not func_(val1, val2):
                            return False

        except KeyError as e:
            raise InvalidOperatorError(f'You tried to use an operator that was not allowed ({e.args}).')
        return True

    def value(self, val, components):
        if isinstance(val, str):
            val_component = [c for c in components if c.component_type == self.name]

            if val_component:
                self.log.trace(f'Getting value for "{val}" in {val_component[0].declaration}')
                return val_component[0].declaration.get(val)
            else:
                return None

    @classmethod
    def from_dict(cls, rule_dict):
        return cls(
            name=rule_dict.get('name', ValueError),
            criteria=rule_dict.get('criteria', MissingCriteriaError)
        )

