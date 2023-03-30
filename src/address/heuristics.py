import logging
import math
from typing import List, Tuple, Optional

from src.exceptions import InconclusiveEvaluationException


class AddressHeuristics:
    """
    This class defines a set of heuristics to evaluate whether a token matches certain
    patterns. The class has three methods to add heuristics: add_bool, add_count, and
    add_distance. These methods take in certain parameters and generate functions that
    will be added to the list of heuristics.

    The evaluate method is used to evaluate a single token using all the heuristics added
    to the instance. This method takes in keyword arguments representing the token,
    position, count, and other values required by the heuristics. The method applies
    each of the heuristics to the input and calculates a confidence score based on how
    many of the heuristics matched the input. The method returns a tuple with a boolean
    value indicating whether the input matched the heuristics and a float indicating the
    confidence score.

    If no heuristics match the input, the method raises an InconclusiveEvaluationException.
    """
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.heuristics = []

    def add_bool(self, **kwargs) -> None:
        def function() -> Tuple:
            return kwargs.get('operation')(*kwargs.get('values')), kwargs.get('multiplier')

        self.log.trace(f"Add boolean check for: {kwargs.get('operation')}. Using values: {kwargs.get('values')}")
        self.log.trace(f"Multiplier for check is: {kwargs.get('multiplier')}")
        self.heuristics.append(function)

    def add_count(self, **kwargs) -> None:
        def function() -> Tuple:
            count = 0
            for v in kwargs.get('list'):
                if 'values' in kwargs.keys():
                    v = [v] + [w for w in kwargs.get('values')]
                if kwargs.get('operation')(*v):
                    count += 1
                else:
                    count -= 1

            result = (count > 0)
            if 'target' in kwargs.keys():
                count = math.sqrt(math.pow((count - kwargs.get('target')), 2))

            score = 1 + (count * kwargs.get('multiplier'))

            return result, score

        self.log.trace(f"Add count check for: {kwargs.get('list')}. Checking if each value is: "
                       f"{kwargs.get('operation')}. Using values: {kwargs.get('values')}")
        self.log.trace(f"Multiplier for check is: {kwargs.get('multiplier')}")
        if 'target' in kwargs.keys():
            self.log.trace(f'Target ')

        self.heuristics.append(function)

    def add_distance(self, **kwargs) -> None:
        def function() -> Tuple:
            count = math.sqrt(math.pow(kwargs.get('count') - kwargs.get('target'), 2))
            score = 1 / (count * kwargs.get('multiplier') + 1)
            return True, score

        self.heuristics.append(function)

    def evaluate(self, **kwargs) -> Tuple[bool, float]:
        """
        Evaluate a single token using all heuristics.

        Args:
        token (str): The token to evaluate.
        position (int): The position of the token in the input.

        Returns:
        A tuple of a boolean indicating whether the token matches the heuristics and a float indicating the confidence in the match.
        """
        confidence_set = []
        no_confidence_set = []
        confidence = 1.0
        no_confidence = 1.0
        for heuristic in self.heuristics:
            result, score = heuristic(**kwargs)
            if result:
                confidence *= score
                confidence_set.append(True)
            else:
                no_confidence *= score
                no_confidence_set.append(True)

        diff = no_confidence - confidence

        if no_confidence > confidence and any(no_confidence_set):
            return False, diff
        elif confidence > no_confidence and any(confidence_set):
            return True, -diff
        else:
            raise InconclusiveEvaluationException(f'Unable to determine if "{kwargs.get("token")}" matches any heuristic')

