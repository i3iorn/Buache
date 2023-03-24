import operator

from typing import Any

from v2.rule.parser import Parser

__all__ = [
    'Parser',
    'Rule'
]


class Rule:
    OPERATORS = {
        'is': (operator.is_, 2),
        'gt': (operator.gt, 2)
    }

    def __init__(self):
        pass

    def asserts(self, assert_type, values: Any) -> bool:
        func_, vals = self.OPERATORS[assert_type]
        assert func_(*values[:vals])

        return True

    def evaluate(self):
        pass
