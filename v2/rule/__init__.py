import logging
import operator

from typing import Any, List, Dict, Tuple, Union

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
        'isalnum': (str.isalnum, 1),
        'endswith': (str.endswith, 2),
        'startswith': (str.startswith, 2),
        'notequal': (operator.ne, 2)
    }

    def __init__(self, name: str = None):
        """
        Initializes a new instance of the Rule class.

        Args:
            name (str): The name of the rule.

        Raises:
            ValueError: If name is not provided.
        """
        self._min = None
        self._max = None
        self.log = logging.getLogger(__name__)
        self._criteria = None
        if name is None:
            raise ValueError(f'A rule must have a name.')
        else:
            self.name = name

    @property
    def criteria(self) -> dict:
        if self.saved() and self._criteria is None:
            self._load_rule_from_file()
        return self._criteria

    @criteria.setter
    def criteria(self, value: dict) -> None:
        self._criteria = value

    @property
    def min(self) -> int:
        if self.saved() and self._min is None:
            self._load_rule_from_file()
        return self._min

    @min.setter
    def min(self, value: int) -> None:
        self._min = value

    @property
    def max(self) -> int:
        if self.saved() and self._max is None:
            self._load_rule_from_file()
        return self._max

    @max.setter
    def max(self, value: int) -> None:
        self._max = value

    def _load_rule_from_file(self):
        if self.saved():
            self.log.trace(f'Load rule {self.name}')
            parsed_rule = Parser.load(name=self.name)[0]
            self.related_rules = Parser.load(rfilter=[parsed_rule['flags']])
            self.criteria = parsed_rule['criteria']
            self.min = parsed_rule['min']
            self.max = parsed_rule['max']

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

    def evaluate(self,
                 address_component_value,
                 compare_to: [str, int] = None,
                 index: int = None,
                 identified_components: List = None,
                 full_address: str = None,
                 word: str = None
                 ) -> Tuple[float, List[str]]:
        """
        Evaluates a rule for an address component.

        Args:
            address_component_value (str): The value of the address component.
            compare_to (str or int): The value to compare the address component to.
            index (int): The index of the address component in the address.
            identified_components (list): The identified components in the address.
            full_address (str): The full address string.
            word (str): The word to match with the address component.

        Returns:
            Tuple[float, List[str]]: A tuple containing the score of the evaluation and a list of matched criteria.
        """
        if not self.saved():
            raise EvaluationException("Can't evaluate a rule that has not been saved.")

        score = 0
        num_criteria = len(self.criteria)
        matched_criteria = []

        for criterion in self.criteria:
            criterion_type = criterion.get('type')

            if criterion_type == 'length':
                score += self._evaluate_length(address_component_value, criterion)
                matched_criteria.append('length')

            elif criterion_type == 'number':
                score += self._evaluate_number(address_component_value, criterion)
                matched_criteria.append('number')

            elif criterion_type == 'position':
                score += self._evaluate_position(criterion, identified_components, index)
                matched_criteria.append('position')

            elif criterion_type == 'string_type':
                score += self._evaluate_string_type(address_component_value, criterion)
                matched_criteria.append('string_type')

            elif criterion_type == "endswith":
                score += self._evaluate_endswith(address_component_value, criterion, word)
                matched_criteria.append('endswith')

            elif criterion_type == "startswith":
                score += self._evaluate_startswith(address_component_value, criterion, word)
                matched_criteria.append('startswith')

            elif criterion_type == 'notequal':
                score += self._evaluate_notequal(address_component_value, criterion, compare_to)
                matched_criteria.append('notequal')

            else:
                raise CriteriaTypeError(f'"{criterion_type}" is an invalid criteria type.', criterion_type)

        self._evaluate_word_match(address_component_value, word, score, criterion)

        final_score = score / num_criteria

        self.log.trace(
            f'Ran evaluation for "{address_component_value}" against "{self.name}". Resulting in {final_score}')

        return final_score, matched_criteria

    def _evaluate_length(self, address_component_value, criterion):
        """
        Evaluates the length criterion.

        Args:
            address_component_value (str): The value of the address component.
            criterion (dict): The criterion to evaluate.

        Returns:
            float: The score of the evaluation.
        """
        try:
            self.asserts('gt', [len(address_component_value), int(criterion.get('min'))])
            self.asserts('lt', [len(address_component_value), int(criterion.get('max'))])
            return self.calculate_score(criterion, True)
        except AssertionError:
            return self.calculate_score(criterion, False)

    def _evaluate_number(self, address_component_value, criterion):
        """
        Evaluates the number criterion.

        Args:
            address_component_value (str): The value of the address component.
            criterion (dict): The criterion to evaluate.

        Returns:
            float: The score of the evaluation.
        """
        if address_component_value.isnumeric():
            try:
                self.asserts('gt', [int(address_component_value), int(criterion.get('min'))])
                self.asserts('lt', [int(address_component_value), int(criterion.get('max'))])
                return self.calculate_score(criterion, True)
            except AssertionError:
                return self.calculate_score(criterion, False)
        else:
            return self.calculate_score(criterion, False)

    def _evaluate_position(self, criterion: Dict, identified_components: List, index: int) -> float:
        """
        Evaluate the position criterion of the rule against a component at the given index.
        """
        score = 0

        for oper in ['gt', 'lt']:
            for component in criterion.get(oper, []):
                if identified_components:
                    matching_components = [ic for ic in identified_components if component == ic.component_type]
                    if matching_components:
                        ec = matching_components[0]
                        try:
                            self.asserts(oper, [index, ec.position])
                            score += self.calculate_score(criterion, True)
                        except AssertionError:
                            score += self.calculate_score(criterion, False)
                            continue

        return score

    def _evaluate_string_type(self, address_component_value, criterion) -> Tuple[float, bool]:
        """
        Evaluate a criterion of type "string_type" against an address component value.

        Args:
            address_component_value (str): The value of the address component to evaluate.
            criterion (dict): The criterion of type "string_type" to evaluate.

        Returns:
            A tuple containing the score (float) and a boolean indicating if the criterion was met or not.
        """
        string_type = criterion.get('string_type')
        criterion_met = False

        # Check if address_component_value matches the string type
        if string_type == 'alpha':
            criterion_met = address_component_value.isalpha()
        elif string_type == 'alphanum':
            criterion_met = address_component_value.isalnum()
        elif string_type == 'numeric':
            criterion_met = address_component_value.isnumeric()

        # Calculate score based on criterion_met
        score = self.calculate_score(criterion, criterion_met)

        return score

    def _evaluate_endswith(self, address_component_value: str, criterion: dict, word: str) -> float:
        """
        Evaluate the address component value against the given criterion of type "endswith".

        Parameters:
        address_component_value (str): The value of the address component to evaluate.
        criterion (dict): The criterion of type "endswith" to use for the evaluation.
        word (str): The word to compare to the end of the address component value.

        Returns:
        float: The score for this evaluation, as a float between 0 and 1.
        """
        if word is not None:
            self.log.debug(f'Endswith: {word}, {address_component_value}')
            if address_component_value.endswith(word):
                self.asserts(criterion.get('type'), [word, address_component_value])
                return self.calculate_score(criterion, True)
        return self.calculate_score(criterion, False)

    def _evaluate_startswith(self, address_component_value: str, criterion: dict, word: str) -> float:
        """
        Evaluates whether the address component value starts with a given word, according to a given criterion.
        Returns a score between 0 and 1.

        Args:
            address_component_value: The address component value to be evaluated.
            criterion: The criterion to be used for evaluation.
            word: The word to be compared with the address component value.

        Returns:
            float: A score between 0 and 1 representing the level of compliance with the given criterion.
        """
        # Check if a word is provided for comparison
        if word is not None:
            self.log.debug(f'Starts with: {word}, {address_component_value}')
            # Check if the address component value starts with the given word
            if address_component_value.startswith(word):
                # Calculate and return the score for compliance with the criterion
                return self.calculate_score(criterion, True)

        # If the address component value does not start with the given word, calculate and return the score for
        # non-compliance
        return self.calculate_score(criterion, False)

    def _evaluate_notequal(self, address_component_value: str, compare_to: Union[str, int], criterion: Dict) -> float:
        """
        Evaluates a 'notequal' criterion type for an address component value.

        Args:
            address_component_value (str): The value of the address component to be evaluated.
            compare_to (Union[str, int]): The value to compare the address component value to.
            criterion (Dict): The criterion being evaluated.

        Returns:
            float: The score obtained for the evaluation.

        Raises:
            AssertionError: If the criterion is not met.

        """
        try:
            self.asserts('notequal', [address_component_value, compare_to])
            score = self.calculate_score(criterion, True)
        except AssertionError:
            score = self.calculate_score(criterion, False)

        return score

    def _evaluate_word_match(self, address_component_value: str, word: str, score: float, criterion: dict) -> float:
        """
        Evaluate the 'word match' criterion type and update the score accordingly.

        Args:
            address_component_value (str): The address component value to evaluate.
            word (str): The word to compare against.
            score (float): The current score.
            criterion (dict): The criterion to evaluate.

        Returns:
            float: The updated score.
        """
        try:
            if self.asserts('is', [word, address_component_value]):
                score += self.calculate_score(criterion, True)
        except AssertionError as e:
            score += self.calculate_score(criterion, False)

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

    @staticmethod
    def calculate_score(crit: dict, passed: bool) -> int:
        multiplier = 1
        if not passed:
            multiplier *= -1
        if crit.get('required'):
            multiplier *= 2
        if crit.get('primary'):
            multiplier *= 2

        return crit.get('score', 1) * multiplier

