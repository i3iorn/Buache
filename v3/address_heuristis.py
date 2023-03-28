from typing import List, Tuple

from v3.exceptions import InconclusiveEvaluationException


class AddressHeuristics:
    def __init__(self):
        self.heuristics = []

    def add_heuristic(self, heuristic):
        self.heuristics.append(heuristic)

    def evaluate_token(self, **kwargs) -> Tuple[bool, float]:
        """
        Evaluate a single token using all heuristics.

        Args:
        token (str): The token to evaluate.
        position (int): The position of the token in the input.

        Returns:
        A tuple of a boolean indicating whether the token matches the heuristics and a float indicating the confidence in the match.
        """
        confidence = 1.0
        no_confidence = 1.0
        for heuristic in self.heuristics:
            result, score = heuristic(**kwargs)
            if result:
                confidence *= score
            else:
                no_confidence *= score
        if no_confidence > confidence:
            return False, no_confidence
        elif confidence > no_confidence:
            return True, confidence
        else:
            raise InconclusiveEvaluationException(f'Unable to determine if "{kwargs.get("token")}" matches any heuristic')

    def evaluate(self, tokens: List[str]) -> Tuple[bool, float]:
        """
        Evaluate a list of tokens using all heuristics.

        Args:
        tokens (List[str]): The list of tokens to evaluate.

        Returns:
        A tuple of a boolean indicating whether all tokens match the heuristics and a float indicating the confidence in the match.
        """
        confidence = 1.0
        no_confidence = 1.0
        for i, token in enumerate(tokens):
            result, score = self.evaluate_token(token, i)
            if result:
                confidence *= score
            else:
                no_confidence *= score
        if no_confidence > confidence:
            return False, no_confidence
        elif confidence > no_confidence:
            return True, confidence
        else:
            raise InconclusiveEvaluationException(f'Unable to determine if "{tokens}" matches any heuristic')
