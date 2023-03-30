import logging
import math
from typing import List, Tuple, Optional

from src.exceptions import InconclusiveEvaluationException, ComponentEvaluationException


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
            return kwargs.get('operation')(*kwargs.get('values')), float(kwargs.get('multiplier'))

        self.log.trace(f"Add boolean check for: {kwargs.get('operation')}. \nUsing values: {kwargs.get('values')}"
                       f"\nMultiplier is set to: {kwargs.get('multiplier')}")
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

            score = 1 + (count * float(kwargs.get('multiplier')))

            return result, score

        msg = f"Add count check for: {kwargs.get('list')}. " \
              f"\nChecking if each value is: {kwargs.get('operation')}. " \
              f"\nUsing values: {kwargs.get('values')}" \
              f"\nMultiplier for check is: {kwargs.get('multiplier')}"

        if 'target' in kwargs.keys():
            msg += f"\nTarget: {kwargs.get('target')}"

        self.log.trace(msg)

        self.heuristics.append(function)

    def add_distance(self, **kwargs) -> None:
        def function() -> Tuple:
            count = math.sqrt(math.pow(kwargs.get('count') - kwargs.get('target'), 2))
            score = 1 / (count * float(kwargs.get('multiplier')) + 1)
            return True, score

        self.log.trace(f"Add distance check between {kwargs.get('count')} and {kwargs.get('target')}. "
                       f"Multiplier is: {kwargs.get('multiplier')}")
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
        self.log.trace(f'Checking {len(self.heuristics)} heuristics.')

        confidence_set = []
        no_confidence_set = []
        confidence = 1.0
        no_confidence = 1.0
        try:
            for heuristic in self.heuristics:
                result, score = heuristic(**kwargs)
                if result:
                    confidence *= score
                    confidence_set.append(True)
                else:
                    no_confidence *= score
                    no_confidence_set.append(True)
        except TypeError as e:
            self.log.warning(f'Confidence: {confidence}')
            self.log.warning(f'No Confidence: {no_confidence}')
            self.log.warning(f'Confidence is set: {confidence_set}')
            self.log.warning(f'Confidence: {no_confidence_set}')
            self.log.warning(f'Score: {score}')
            raise ComponentEvaluationException from e

        diff = no_confidence - confidence

        if no_confidence > confidence and any(no_confidence_set):
            self.log.debugx(f'Tests failed with confidence: {no_confidence}')
            return False, diff
        elif confidence > no_confidence and any(confidence_set):
            self.log.debugx(f'Tests passed with confidence: {confidence}')
            return True, -diff
        else:
            self.log.debug(f'Tests were inconclusive.')
            raise InconclusiveEvaluationException(f'Unable to determine if "{kwargs.get("token")}" matches any heuristic')

