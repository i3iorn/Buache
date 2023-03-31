import logging
import math
from typing import List, Tuple, Optional

from src.exceptions import InconclusiveEvaluationException, ComponentEvaluationException


class AddressHeuristics:
    """
    This class contains heuristics used to evaluate whether a token matches certain patterns.
    The heuristics can be added using the add_bool, add_count, and add_distance methods.
    The evaluate method applies all heuristics to the input and calculates a confidence score based on how
    many of the heuristics matched the input. If no heuristics match the input, the method raises an
    InconclusiveEvaluationException.

    Attributes:

        log: a logging instance.
        heuristics: a list to store the heuristics to be evaluated.

    Methods:

        add_bool: add a boolean check to the heuristics list.
        add_count: add a count check to the heuristics list.
        add_distance: add a distance check to the heuristics list.
        evaluate: evaluate a single token using all heuristics in the list.

    Exceptions:

        InconclusiveEvaluationException: raised when no heuristics match the input.
        ComponentEvaluationException: raised when an error occurs during heuristic evaluation.
    """
    def __init__(self):
        """
        Initializes an instance of the AddressHeuristics class.
        """

        self.log = logging.getLogger(__name__)
        self.heuristics = []

    def add(self, heuristic_type, **kwargs):
        func = getattr(self, f'add_{heuristic_type}', 'add_bool')
        func(**kwargs)

    def add_bool(self, **kwargs) -> None:
        """
        Adds a boolean heuristic function to the heuristics list.

        Args:
            kwargs: keyword arguments representing the function parameters.

        Returns:
            None.
        """

        def function() -> Tuple:
            return kwargs.get('operation')(*kwargs.get('values')), float(kwargs.get('multiplier'))

        self.log.trace(f"Add boolean check for: {kwargs.get('operation')}. \nUsing values: {kwargs.get('values')}"
                       f"\nMultiplier is set to: {kwargs.get('multiplier')}")
        self.heuristics.append(function)

    def add_count(self, **kwargs) -> None:

        """
        Adds a count heuristic function to the heuristics list.

        Args:
            kwargs: keyword arguments representing the function parameters.

        Returns:
            None.
        """

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
        """
        Adds a distance heuristic function to the heuristics list.

        Args:
            kwargs: keyword arguments representing the function parameters.

        Returns:
            None.
        """

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
        for heuristic in self.heuristics:
            try:
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
                self.log.warning(f'Heuristic: {heuristic}')
                raise ComponentEvaluationException from e

        diff = no_confidence - confidence

        if no_confidence > confidence and any(no_confidence_set):
            self.log.debugx(f'Tests failed with confidence: {no_confidence}')
            return False, diff
        elif confidence > no_confidence and any(confidence_set):
            self.log.debugx(f'Tests passed with confidence: {confidence}')
            return True, -diff
        else:
            self.log.debugx(f'Tests were inconclusive.')
            raise InconclusiveEvaluationException(f'Unable to determine if "{kwargs.get("token")}" matches any heuristic')

