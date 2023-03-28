import re
import math
from typing import Tuple, List, Optional

from v3.address_heuristis import AddressHeuristics
from v3.exceptions import InconclusiveEvaluationException


class AddressParserHelperClass:
    def __init__(self):
        pass

    def is_street_number(self, token: str, position) -> Tuple[bool, float]:
        """Determine whether the input string represents a street number."""

        address_heuristics = AddressHeuristics()
        def is_number(**kwargs): return kwargs['token'].isdigit, 1.1
        address_heuristics.add_heuristic(is_number)
        def gt(**kwargs): return kwargs.get('len') > kwargs.get('gt_val'), 1.1
        address_heuristics.add_heuristic(gt)
        def lt(**kwargs): return kwargs.get('len') < kwargs.get('lt_val'), 1.1
        address_heuristics.add_heuristic(gt)

        return address_heuristics.evaluate_token(
            token=token,
            len=len(token),
            gt_val=1,
            lt_val=5
        )

    def is_street_name(self, token: str, position) -> Tuple[bool, float]:
        """Determine whether the input string represents a street name."""
        confidence = 1.0
        no_confidence = 1.0

        if len(token) < 3:
            no_confidence *= 3
        elif len(token) > 50:
            no_confidence *= 1.5
        elif position == 0:
            confidence *= 1 + (len(token) / 10)

        if token[0].islower():
            # Street names are typically capitalized.
            no_confidence *= 1.2
        else:
            confidence *= 1.2

        if token.isdigit():
            # Street names don't consist only of digits.
            no_confidence *= 5

        if not token[0].isalpha():
            # Street names should start and end with a letter.
            no_confidence *= 5
        if not token[-1].isalpha():
            no_confidence *= 2
            confidence /= 1.5

        no_confidence *= 1 + position / 10

        # TODO: Add more heuristics
        if no_confidence > confidence:
            result = False, no_confidence
        elif confidence > no_confidence:
            result = True, confidence
        else:
            raise InconclusiveEvaluationException(f'Unable to determine if "{token}" is a country')

        return result

    def is_city(self, token: str, position) -> Tuple[bool, float]:
        """Determine whether the input string represents a city name."""
        confidence = 1.0
        no_confidence = 1.0
        token = token.strip().lower()
        if len(token) < 3:
            # City names are typically longer than 2 and shorter than 50 characters.
            no_confidence *= 3
        if len(token) > 50:
            no_confidence *= 1.5

        if token.isdigit():
            # City names don't consist only of digits.
            no_confidence *= 5
        else:
            confidence *= 1.1

        if not token[0].isalpha() or not token[-1].isalpha():
            # City names should start and end with a letter.
            no_confidence *= 1.1
            confidence /= 1.1
        else:
            confidence *= 1.1

        if token[0].islower():
            # City names are typically capitalized.
            no_confidence *= 1.1
        else:
            confidence *= 1.1

        for c in token:
            count = 0
            if c.isdigit() or c.isspace():
                count += 1

            confidence /= 1 + count / 10

        confidence *= 1 + position / 10

        # TODO: Add more heuristics
        if no_confidence > confidence:
            result = False, no_confidence
        elif confidence > no_confidence:
            result = True, confidence
        else:
            raise InconclusiveEvaluationException(f'Unable to determine if "{token}" is a country')

        return result

    def is_postal_code(self, token, position) -> Tuple[bool, float]:
        """
        Determine whether the given text is a valid postal code.

        Args:
        text (str): The text to check.

        Returns:
        bool: True if the text is a valid postal code, False otherwise.
        """
        confidence = 1.0
        no_confidence = 1.0
        # Check if the text matches the postal code regex
        regex = re.compile(r"\b\d{5}(?:[-\s]\d{4})?\b")
        if regex.search(token):
            confidence *= 2
        else:
            no_confidence *= 1.5

        # TODO: Add more heuristics
        if no_confidence > confidence:
            result = False, no_confidence
        elif confidence > no_confidence:
            result = True, confidence
        else:
            raise InconclusiveEvaluationException(f'Unable to determine if "{token}" is a country')

        return result

    def is_block(self, token, position) -> Tuple[bool, float]:
        """
        Returns True if the given token represents a block number, False otherwise.
        """
        confidence = 1.0
        # Check if the token starts with a number followed by a dash and another number (e.g. 123-45)
        if '-' in token:
            parts = token.split('-')
            if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                return True, confidence

        # Check if the token starts with a number followed by a slash and another number (e.g. 123/45)
        if '/' in token:
            parts = token.split('/')
            if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                return True, confidence

        return False, confidence

    def is_apartment(self, token, position) -> Tuple[bool, float]:
        """
        Returns True if the given token represents a block number, False otherwise.
        """
        confidence = 1.0
        # Check if the token is all digits and has a length between 1 and 4 (block numbers are typically short)
        if token.isdigit() and 1 <= len(token) == 4:
            return True, confidence

        return False, confidence

    def is_co(self, token, position) -> Tuple[bool, float]:
        confidence = 1.0
        no_confidence = 1.0
        # TODO: Add more heuristics
        if no_confidence > confidence:
            result = False, no_confidence
        elif confidence > no_confidence:
            result = True, confidence
        else:
            raise InconclusiveEvaluationException(f'Unable to determine if "{token}" is a country')

        return result

    def is_entrance(self, token, position) -> Tuple[bool, float]:
        confidence = 1.0
        # Check if the token starts with a number followed by a letter (e.g. 1A, 2B)
        if len(token) == 2 and token[0].isdigit() and token[1].isalpha():
            return True, confidence

        return False, confidence

    def is_building(self, token, position) -> Tuple[bool, float]:
        confidence = 1.0
        no_confidence = 1.0
        # TODO: Add more heuristics
        if no_confidence > confidence:
            result = False, no_confidence
        elif confidence > no_confidence:
            result = True, confidence
        else:
            raise InconclusiveEvaluationException(f'Unable to determine if "{token}" is a country')

        return result

    def is_state(self, token, position) -> Tuple[bool, float]:
        confidence = 1.0
        no_confidence = 1.0
        # TODO: Add more heuristics
        if no_confidence > confidence:
            result = False, no_confidence
        elif confidence > no_confidence:
            result = True, confidence
        else:
            raise InconclusiveEvaluationException(f'Unable to determine if "{token}" is a country')

        return result

    def is_country(self, token, position) -> Tuple[bool, float]:
        confidence = 1.0
        no_confidence = 1.0
        # TODO: Add more heuristics
        if no_confidence > confidence:
            result = False, no_confidence
        elif confidence > no_confidence:
            result = True, confidence
        else:
            raise InconclusiveEvaluationException(f'Unable to determine if "{token}" is a country')

        return result
