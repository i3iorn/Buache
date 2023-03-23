import logging
from typing import Optional, List

from src import Rule


class AddressComponent:
    """
    A class representing a component of an address, such as the street, city, or postal code.

    :param component_type: The type of the address component, such as 'street', 'city', or 'postal_code'.
    :param value: The value of the address component, such as '123 Main St' or 'New York'.
    """
    def __init__(
        self,
        value: str,
        component_type: str,
        index: int,
        rules: Optional[List[Rule]] = None
    ):

        self.component_type = component_type
        self.value = value

    def validate(self) -> bool:
        """
        Validate that the address component has valid data.

        :return: True if the component is valid, False otherwise.
        """
        # TODO: Implement validation logic
        # Example validation:
        if self.value is None or len(self.value.strip()) == 0:
            logging.warning(f"{self.component_type} has no value.")
            return False

        if not self.value.isalnum():
            logging.warning(f"{self.component_type} is not alphanumeric.")
            return False

        return True

    def format(self) -> str:
        """
        Format the address component into a string.

        :return: A string representing the address component.
        """
        # TODO: Implement formatting logic
        # Example formatting:
        return self.value
