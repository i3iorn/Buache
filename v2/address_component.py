import logging

from v2.config import ADDRESS_COMPONENT_TYPES


class AddressComponent:
    """
    Represents a single component of an address, such as a street name, number, or postal code.

    Attributes:
        component_type (str): The type of the address component, as defined in ADDRESS_COMPONENT_TYPES.
        position (int): The position of the component within the address.
        value (str): The value of the component.

    Raises:
        ValueError: If any of the required parameters are missing or None.
    """
    def __init__(self,
                 ad_type: ADDRESS_COMPONENT_TYPES = None,
                 position: int = None,
                 value: str = None
                 ):
        self.log = logging.getLogger(__name__)

        if not all([ad_type, position, value]):
            raise ValueError(f'ad_type, position, value all needs to have a value.')

        self.component_type = ad_type
        self.position = position
        self.value = value
