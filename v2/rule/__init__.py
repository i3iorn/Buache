import logging
import operator

from typing import Any, List

from v2.exceptions import EvaluationException, CriteriaTypeError

__all__ = [
    'Rule'
]

from v2.rule.parser import Parser


class Rule:
    """
    Represents a rule.

    Attributes:
        name (str): The name of the rule.

    Constants:
        OPERATORS (dict): A dictionary mapping operator strings to corresponding operator functions and required argument counts.
            Example: {
                'is': (operator.is_, 2),
                'gt': (operator.gt, 2)
            }
    """
    OPERATORS = {
        'is': (operator.is_, 2),
        'gt': (operator.gt, 2),
        'lt': (operator.lt, 2),
        'isnumeric': (str.isnumeric, 1),
        'isalpha': (str.isalpha, 1),
        'isalnum': (str.isalnum, 1)
    }

    def __init__(self, name: str = None):
        """
        Initializes a new instance of the Rule class.

        Args:
            name (str): The name of the rule.

        Raises:
            ValueError: If name is not provided.
        """
        self.log = logging.getLogger(__name__)
        self._criteria = None
        if name is None:
            raise ValueError(f'A rule must have a name.')
        else:
            self.name = name

        self._load_rule_from_file()

    @property
    def criteria(self) -> dict:
        if self.saved() and self._criteria is None:
            self._load_rule_from_file()
        return self._criteria

    @criteria.setter
    def criteria(self, value: dict) -> None:
        self._criteria = value

    def _load_rule_from_file(self):
        if self.saved():
            self.log.debug(f'Load rules from file')
            parsed_rule = Parser.load(name=self.name)[0]
            self.related_rules = Parser.load(rfilter=[parsed_rule['flags']])
            self.criteria = parsed_rule['criteria']

    def asserts(self, assert_type, values: List[Any]) -> bool:
        """
        Determines whether a given assert type and values satisfy this rule's condition.

        Args:
            assert_type (str): The type of assert to evaluate.
            values (Any): The value(s) to evaluate against the assertion.

        Returns:
            bool: True if the condition is satisfied, False otherwise.
        """
        func_, vals = self.OPERATORS[assert_type]
        assert func_(*values[:vals])

        return True

    def evaluate(self, eval_value, index, identified_components: List) -> bool:
        """
        Evaluates this rule.
        """
        if not self.saved():
            raise EvaluationException(f"Can't evaluate a rule that has not been saved.")

        score = 0

        for crit in self.criteria:
            crit_type = crit.get('type')
            if crit_type == 'length':
                try:
                    self.asserts('gt', [len(eval_value), crit.get('min')])
                    self.asserts('lt', [len(eval_value), crit.get('max')])
                    score = crit.get('score', 1)
                except AssertionError:
                    score = crit.get('score', 1) * -1

            elif crit_type == 'number':
                try:
                    if eval_value.isnumeric():
                        self.asserts('gt', [int(eval_value), crit.get('min')])
                        self.asserts('lt', [int(eval_value), crit.get('max')])
                        score = crit.get('score', 1)
                except AssertionError:
                    score = crit.get('score', 1) * -1

            elif crit_type == 'position':
                if len(identified_components) > 0:
                    try:
                        for oper in ['gt', 'lt']:
                            for component in crit.get(oper, []):
                                ec = [ic for ic in identified_components if component == ic.component_type][0]
                                if ec:
                                    self.asserts(oper, [index, ec.position])
                                    score = crit.get('score', 1)
                    except AssertionError:
                        score = crit.get('score', 1) * -1

            elif crit_type == 'string_type':
                try:
                    self.asserts(crit.get('string_type'), [eval_value])
                    score = crit.get('score', 1)
                except AssertionError:
                    score = crit.get('score', 1) * -1

            else:
                raise CriteriaTypeError(f'"{crit_type}" is an invalid criteria type.')

        return score

    def saved(self) -> bool:
        """
        Determines whether this rule exists in the parser.

        Returns:
            bool: True if the rule exists, False otherwise.
        """
        return len(Parser.load(name=self.name)) == 1

    @staticmethod
    def available_rules():
        return [r.get("name") for r in Parser.load()]
