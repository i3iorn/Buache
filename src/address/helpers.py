import inspect
import operator
from typing import Tuple

from config import CONFIG
from src.address.heuristics import AddressHeuristics


def is_street_number(token: str, position, full_address: str = None) -> Tuple[bool, float]:
    """Determine whether the input string represents a street number."""
    section = f'heuristics.{inspect.currentframe().f_code.co_name}'
    address_heuristics = AddressHeuristics()
    address_heuristics.add_bool(
        operation=str.isdigit,
        multiplier=CONFIG.get(section, 'str_isdigit_token'), values=[token])
    address_heuristics.add_bool(
        operation=operator.gt,
        multiplier=CONFIG.get(section, 'operator_gt_len_token'), values=[len(token), 0])
    address_heuristics.add_bool(
        operation=operator.lt,
        multiplier=CONFIG.get(section, 'operator_lt_len_token'), values=[len(token), 5])
    address_heuristics.add_distance(
        multiplier=CONFIG.get(section, 'distance_position_2'), count=position, target=2)
    address_heuristics.add_distance(
        multiplier=CONFIG.get(section, 'distance_len_token_1'), count=len(token), target=1)

    if token.isdigit():
        address_heuristics.add_bool(
            operation=operator.gt,
            multiplier=CONFIG.get(section, 'operator_gt_token_0'), values=[int(token), 0])

    return address_heuristics.evaluate()


def is_street_name(token: str, position: int, full_address: str = None) -> Tuple[bool, float]:
    """Determine whether the input string represents a street name."""

    print(CONFIG.sections())
    section = f'heuristics.{inspect.currentframe().f_code.co_name}'

    address_heuristics = AddressHeuristics()
    address_heuristics.add_bool(operation=str.isupper,
                                multiplier=CONFIG.get(section, 'str_isupper_token_first'),
                                values=[token[0]])
    address_heuristics.add_bool(operation=str.isalpha,
                                multiplier=CONFIG.get(section, 'str_isalpha_token_first'),
                                values=[token[0]])
    address_heuristics.add_bool(operation=str.isalpha,
                                multiplier=CONFIG.get(section, 'str_isalpha_token_last'),
                                values=[token[-1]])
    address_heuristics.add_bool(operation=operator.gt,
                                multiplier=CONFIG.get(section, 'operator_gt_len_token'),
                                values=[len(token), 3])
    address_heuristics.add_bool(operation=operator.lt,
                                multiplier=CONFIG.get(section, 'operator_lt_len_token'),
                                values=[len(token), 30])
    address_heuristics.add_count(operation=operator.truth,
                                 multiplier=CONFIG.get(section, 'operator_truth_list_token'),
                                 list=list(token),
                                 target=len(full_address))
    address_heuristics.add_distance(multiplier=CONFIG.get(section, 'str_isupper_token_first'),
                                    count=position, target=0)

    return address_heuristics.evaluate()


def is_city(token: str, position, full_address: str = None) -> Tuple[bool, float]:
    """Determine whether the input string represents a city name."""

    address_heuristics = AddressHeuristics()
    address_heuristics.add_bool(operation=str.isalpha, multiplier=2.0, values=[token])
    address_heuristics.add_bool(operation=str.isupper, multiplier=1.2, values=[token[0]])
    address_heuristics.add_bool(operation=str.isalpha, multiplier=2.0, values=[token[0]])
    address_heuristics.add_bool(operation=str.isalpha, multiplier=1.3, values=[token[-1]])
    address_heuristics.add_bool(operation=operator.gt, multiplier=1.5, values=[len(token), 3])
    address_heuristics.add_bool(operation=operator.lt, multiplier=1.5, values=[len(token), 40])
    address_heuristics.add_distance(multiplier=0.1, count=position, target=6)

    return address_heuristics.evaluate()


def is_postal_code(token, position, full_address: str = None) -> Tuple[bool, float]:
    """
    Determine whether the given text is a valid postal code.

    Args:
    text (str): The text to check.

    Returns:
    bool: True if the text is a valid postal code, False otherwise.
    """

    address_heuristics = AddressHeuristics()
    address_heuristics.add_bool(operation=str.isdigit, multiplier=3.0, values=[token])
    address_heuristics.add_bool(operation=operator.gt, multiplier=1.5, values=[len(token), 4])
    address_heuristics.add_bool(operation=operator.lt, multiplier=1.5, values=[len(token), 8])
    address_heuristics.add_distance(multiplier=0.1, count=position, target=5)

    return address_heuristics.evaluate()


def is_block(token, position, full_address: str = None) -> Tuple[bool, float]:
    """
    Returns True if the given token represents a block number, False otherwise.
    """

    address_heuristics = AddressHeuristics()
    address_heuristics.add_count(operation=operator.eq, multiplier=0.2, list=list(token), values=['/'])
    address_heuristics.add_count(operation=operator.eq, multiplier=0.2, list=list(token), values=['-'])
    address_heuristics.add_bool(operation=operator.gt, multiplier=1.5, values=[len(token), 4])
    address_heuristics.add_bool(operation=operator.lt, multiplier=1.5, values=[len(token), 8])
    address_heuristics.add_distance(multiplier=0.1, count=position, target=4)

    return address_heuristics.evaluate()


def is_apartment(token, position, full_address: str = None) -> Tuple[bool, float]:
    """
    Returns True if the given token represents a block number, False otherwise.
    """

    address_heuristics = AddressHeuristics()
    address_heuristics.add_bool(operation=operator.eq, multiplier=2, values=[len(token), 4])
    address_heuristics.add_bool(operation=str.isdigit, multiplier=2, values=[token])
    address_heuristics.add_bool(operation=str.startswith, multiplier=1.1, values=[token.lower(), 'lgh'])
    address_heuristics.add_distance(multiplier=0.1, count=position, target=4)

    return address_heuristics.evaluate()


def is_co(token, position, full_address: str = None) -> Tuple[bool, float]:
    # TODO: Add more heuristics

    return False, 1.0


def is_entrance(token, position, full_address: str = None) -> Tuple[bool, float]:
    address_heuristics = AddressHeuristics()
    address_heuristics.add_bool(operation=operator.lt, multiplier=2, values=[len(token), 3])
    address_heuristics.add_distance(multiplier=0.1, count=position, target=3)
    address_heuristics.add_distance(multiplier=0.4, count=len(token), target=1)
    address_heuristics.add_count(operation=str.isalpha, multiplier=0.2, list=list(token))

    return address_heuristics.evaluate()


def is_building(token, position, full_address: str = None) -> Tuple[bool, float]:
    # TODO: Add more heuristics

    return False, 1.0


def is_state(token, position, full_address: str = None) -> Tuple[bool, float]:
    # TODO: Add more heuristics

    return False, 1.0


def is_country(token, position, full_address: str = None) -> Tuple[bool, float]:
    address_heuristics = AddressHeuristics()
    address_heuristics.add_distance(multiplier=0.1, count=position, target=len(full_address.split()))

    return address_heuristics.evaluate()
