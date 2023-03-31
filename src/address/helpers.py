import inspect
import operator
from typing import Tuple

from config import CONFIG
from src.address.heuristics import AddressHeuristics


def is_(**kwargs):

    multiplier = CONFIG.get(kwargs.get('section'), 'is_digit') or False
    if multiplier:
        kwargs.get('address_heuristics').add_bool(
            operation=str.isdigit,
            multiplier=multiplier,
            values=[kwargs.get('token')])

    multiplier = CONFIG.get(kwargs.get('section'), 'max_length') or False
    if multiplier:
        kwargs.get('address_heuristics').add_bool(
            operation=operator.gt,
            multiplier=multiplier,
            values=[len(kwargs.get('token')), 0])

    multiplier = CONFIG.get(kwargs.get('section'), 'min_length') or False
    if multiplier:
        kwargs.get('address_heuristics').add_bool(
            operation=operator.lt,
            multiplier=multiplier,
            values=[len(kwargs.get('token')), 5])

    multiplier = CONFIG.get(kwargs.get('section'), 'position') or False
    if multiplier:
        kwargs.get('address_heuristics').add_distance(
            multiplier=multiplier,
            count=kwargs.get('position'),
            target=int(CONFIG.get('AddressComponentType', kwargs.get('function_name'))))

    multiplier = CONFIG.get(kwargs.get('section'), 'distance_length') or False
    if multiplier:
        kwargs.get('address_heuristics').add_distance(
            multiplier=multiplier,
            count=len(kwargs.get('token')),
            target=1)

    multiplier = CONFIG.get(kwargs.get('section'), 'capitalized') or False
    if multiplier:
        kwargs.get('address_heuristics').add_bool(
            operation=str.isupper,
            multiplier=multiplier,
            values=[kwargs.get('token')[0]])

    multiplier = CONFIG.get(kwargs.get('section'), 'first_is_letter')
    if multiplier:
        kwargs.get('address_heuristics').add_bool(
            operation=str.isalpha,
            multiplier= multiplier,
            values=[kwargs.get('token')[0]])

    multiplier = CONFIG.get(kwargs.get('section'), 'last_is_letter')
    if multiplier:
        kwargs.get('address_heuristics').add_bool(
            operation=str.isalpha,
            multiplier= multiplier,
            values=[kwargs.get('token')[-1]])

    multiplier = CONFIG.get(kwargs.get('section'), 'operator_gt_len_token')
    if multiplier:
        kwargs.get('address_heuristics').add_bool(
            operation=operator.gt,
            multiplier=multiplier,
            values=[len(kwargs.get('token')), 3])

    multiplier = CONFIG.get(kwargs.get('section'), 'operator_lt_len_token')
    if multiplier:
        kwargs.get('address_heuristics').add_bool(
            operation=operator.lt,
            multiplier=,
            values=[len(kwargs.get('token')), 30])

    multiplier =
    if multiplier:

    multiplier =
    if multiplier:

    kwargs.get('address_heuristics').add_count(
        operation=operator.truth,
        multiplier=CONFIG.get(kwargs.get('section'), 'operator_truth_list_token'),
        list=list(kwargs.get('token')),
        target=len(kwargs.get('full_address', 0)))
    kwargs.get('address_heuristics').add_distance(
        multiplier=CONFIG.get(kwargs.get('section'), 'str_isupper_token_first'),
        count=kwargs.get('position'), target=0)

    return kwargs.get('address_heuristics')


def is_street_number(token: str, position, **kwargs) -> Tuple[bool, float]:
    """Determine whether the input string represents a street number."""
    function_name = inspect.currentframe().f_code.co_name.replace("is_", "")
    section = f'AddressHeuristics.{function_name}'
    address_heuristics = AddressHeuristics()

    address_heuristics = is_(
        address_heuristics=address_heuristics,
        token=token,
        position=position,
        function_name=function_name,
        section=section
    )

    if token.isdigit():
        address_heuristics.add_bool(
            operation=operator.gt,
            multiplier=CONFIG.get(section, 'operator_gt_token_0'), values=[int(token), 0])

    return address_heuristics.evaluate()


def is_street_name(token: str, position: int, **kwargs) -> Tuple[bool, float]:
    """Determine whether the input string represents a street name."""

    function_name = inspect.currentframe().f_code.co_name.replace("is_", "")
    section = f'AddressHeuristics.{function_name}'

    address_heuristics = is_(
        address_heuristics=address_heuristics,
        token=token,
        position=position,
        function_name=function_name,
        section=section
    )

    address_heuristics = AddressHeuristics()

    return address_heuristics.evaluate()


def is_city(token: str, position, **kwargs) -> Tuple[bool, float]:
    """Determine whether the input string represents a city name."""

    function_name = inspect.currentframe().f_code.co_name.replace("is_", "")
    section = f'AddressHeuristics.{function_name}'

    address_heuristics = AddressHeuristics()
    address_heuristics.add_bool(
        operation=str.isalpha,
        multiplier=CONFIG.get(section, 'str_isalpha_token_first'),
        values=[token])
    address_heuristics.add_bool(
        operation=str.isupper,
        multiplier=CONFIG.get(section, 'str_isupper_token_first'),
        values=[token[0]])
    address_heuristics.add_bool(
        operation=str.isalpha,
        multiplier=CONFIG.get(section, 'str_isalpha_token_first'),
        values=[token[0]])
    address_heuristics.add_bool(
        operation=str.isalpha,
        multiplier=CONFIG.get(section, 'str_isalpha_token_last'),
        values=[token[-1]])
    address_heuristics.add_bool(
        operation=operator.gt,
        multiplier=CONFIG.get(section, 'operator_gt_len_token'),
        values=[len(token), 3])
    address_heuristics.add_bool(
        operation=operator.lt,
        multiplier=CONFIG.get(section, 'operator_lt_len_token'),
        values=[len(token), 40])
    address_heuristics.add_distance(
        multiplier=CONFIG.get(section, 'position'),
        count=position,
        target=int(CONFIG.get('AddressComponentType', function_name)))

    return address_heuristics.evaluate()


def is_postal_code(token, position, **kwargs) -> Tuple[bool, float]:
    """
    Determine whether the given text is a valid postal code.

    Args:
    text (str): The text to check.

    Returns:
    bool: True if the text is a valid postal code, False otherwise.
    """

    function_name = inspect.currentframe().f_code.co_name.replace("is_", "")
    section = f'AddressHeuristics.{function_name}'

    address_heuristics = AddressHeuristics()
    address_heuristics.add_bool(
        operation=str.isdigit,
        multiplier=CONFIG.get(section, 'str_isdigit_token'),
        values=[token])
    address_heuristics.add_bool(
        operation=operator.gt,
        multiplier=CONFIG.get(section, 'operator_gt_len_token'),
        values=[len(token), 4])
    address_heuristics.add_bool(
        operation=operator.lt,
        multiplier=CONFIG.get(section, 'operator_lt_len_token'),
        values=[len(token), 8])
    address_heuristics.add_distance(
        multiplier=0.1,
        count=position,
        target=5)
    address_heuristics.add_distance(
        multiplier=CONFIG.get(section, 'position'),
        count=position,
        target=int(CONFIG.get('AddressComponentType', function_name)))

    return address_heuristics.evaluate()


def is_block(token, position, **kwargs) -> Tuple[bool, float]:
    """
    Returns True if the given token represents a block number, False otherwise.
    """

    function_name = inspect.currentframe().f_code.co_name.replace("is_", "")
    section = f'AddressHeuristics.{function_name}'

    address_heuristics = AddressHeuristics()
    address_heuristics.add_count(
        operation=operator.eq,
        multiplier=CONFIG.get(section, 'operator_eq_len_token_slash'),
        list=list(token), values=['/'])
    address_heuristics.add_count(
        operation=operator.eq,
        multiplier=CONFIG.get(section, 'operator_eq_len_token_hyphen'),
        list=list(token), values=['-'])
    address_heuristics.add_bool(
        operation=operator.gt,
        multiplier=CONFIG.get(section, 'operator_gt_len_token'),
        values=[len(token), 4])
    address_heuristics.add_bool(
        operation=operator.lt,
        multiplier=CONFIG.get(section, 'operator_lt_len_token'),
        values=[len(token), 8])
    address_heuristics.add_distance(
        multiplier=CONFIG.get(section, 'position'),
        count=position,
        target=int(CONFIG.get('AddressComponentType', function_name)))

    return address_heuristics.evaluate()


def is_apartment(token, position, **kwargs) -> Tuple[bool, float]:
    """
    Returns True if the given token represents a block number, False otherwise.
    """

    function_name = inspect.currentframe().f_code.co_name.replace("is_", "")
    section = f'AddressHeuristics.{function_name}'

    address_heuristics = AddressHeuristics()
    address_heuristics.add_bool(
        operation=operator.eq,
        multiplier=CONFIG.get(section, 'operator_eq_len_token'),
        values=[len(token), 4])
    address_heuristics.add_bool(
        operation=str.isdigit,
        multiplier=CONFIG.get(section, 'str_isdigit_token'),
        values=[token])
    address_heuristics.add_bool(
        operation=str.startswith,
        multiplier=CONFIG.get(section, 'str_startswith_token_lower_lgh'),
        values=[token.lower(), 'lgh'])
    address_heuristics.add_distance(
        multiplier=CONFIG.get(section, 'position'),
        count=position,
        target=int(CONFIG.get('AddressComponentType', function_name)))

    return address_heuristics.evaluate()


def is_co(token, position, **kwargs) -> Tuple[bool, float]:
    address_heuristics = AddressHeuristics()
    function_name = inspect.currentframe().f_code.co_name.replace("is_", "")
    section = f'AddressHeuristics.{function_name}'

    # TODO: Add more heuristics
    address_heuristics.add_distance(
        multiplier=CONFIG.get(section, 'position'),
        count=position,
        target=int(CONFIG.get('AddressComponentType', function_name)))

    return False, 1.0


def is_entrance(token, position, **kwargs) -> Tuple[bool, float]:
    address_heuristics = AddressHeuristics()
    function_name = inspect.currentframe().f_code.co_name.replace("is_", "")
    section = f'AddressHeuristics.{function_name}'

    address_heuristics.add_bool(
        operation=operator.lt,
        multiplier=CONFIG.get(section, 'operator_lt_len_token'),
        values=[len(token), 3])
    address_heuristics.add_distance(
        multiplier=CONFIG.get(section, 'distance_len_token_4'),
        count=len(token),
        target=1)
    address_heuristics.add_count(
        operation=str.isalpha,
        multiplier=CONFIG.get(section, 'str_isalpha_list_token'),
        list=list(token))
    address_heuristics.add_distance(
        multiplier=CONFIG.get(section, 'position'),
        count=position,
        target=int(CONFIG.get('AddressComponentType', function_name)))

    return address_heuristics.evaluate()


def is_building(token, position, **kwargs) -> Tuple[bool, float]:
    address_heuristics = AddressHeuristics()
    function_name = inspect.currentframe().f_code.co_name.replace("is_", "")
    section = f'AddressHeuristics.{function_name}'

    # TODO: Add more heuristics
    address_heuristics.add_distance(
        multiplier=CONFIG.get(section, 'position'),
        count=position,
        target=int(CONFIG.get('AddressComponentType', function_name)))

    return False, 1.0


def is_state(token, position, **kwargs) -> Tuple[bool, float]:
    address_heuristics = AddressHeuristics()
    function_name = inspect.currentframe().f_code.co_name.replace("is_", "")
    section = f'AddressHeuristics.{function_name}'

    # TODO: Add more heuristics
    address_heuristics.add_distance(
        multiplier=CONFIG.get(section, 'position'),
        count=position,
        target=int(CONFIG.get('AddressComponentType', function_name)))

    return False, 1.0


def is_country(token, position, **kwargs) -> Tuple[bool, float]:
    function_name = inspect.currentframe().f_code.co_name.replace("is_", "")
    section = f'AddressHeuristics.{function_name}'
    address_heuristics = AddressHeuristics()

    address_heuristics.add_distance(
        multiplier=CONFIG.get(section, 'position'),
        count=position,
        target=int(CONFIG.get('AddressComponentType', function_name)))

    address_heuristics.add_bool(
        multiplier=CONFIG.get(section, 'str_is_alpha_token'),
        operation=str.isalpha,
        values=[token])

    return address_heuristics.evaluate()

