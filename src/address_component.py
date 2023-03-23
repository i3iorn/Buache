import logging

from src.declarations import Declaration
from src.exceptions import ComponentThresholdNotReached, AddressComponentException


class AddressComponent:
    """
    A class representing a component of an address, such as the street, city, or postal code.

    :param component_type: The type of the address component, such as 'street', 'city', or 'postal_code'.
    :param value: The value of the address component, such as '123 Main St' or 'New York'.
    :param index: The components placement in the original string.'.
    :param score: How confident we are that we are correct.'.
    """

    def __init__(
            self,
            value: str,
            component_type: str,
            index: int,
            score: int
    ):

        self.declaration = Declaration.read(resource_type='address_component', resource_id=component_type)[0]
        self.component_type = component_type
        self.value = value
        self.index = index
        self.score = score

        try:
            self.validate()
        except AddressComponentException as e:
            raise AddressComponentException(f'Failed to add component: {component_type} with value: {value}') from e

    def validate(self) -> None:
        """
        Validate that the address component has valid data.

        :return: True if the component is valid, False otherwise.
        """
        # Example validation:
        if self.value is None or len(self.value.strip()) == 0:
            logging.warning(f"{self.component_type} has no value.")
            raise AddressComponentException(f"{self.component_type} has no value.")

        if not self.value.isalnum():
            logging.warning(f"{self.component_type} is not alphanumeric.")
            raise AddressComponentException(f"{self.component_type} is not alphanumeric.")
        else:
            if self.declaration.get('string_type') == 'alpha':
                if not self.value.isalpha():
                    logging.warning(f"{self.component_type} is supposed to be letters only.")
                    raise AddressComponentException(f"{self.component_type} is supposed to be letters only.")
            elif self.declaration.get('string_type') == 'num':
                if not self.value.isnumeric():
                    logging.warning(f"{self.component_type} is supposed to be digits only.")
                    raise AddressComponentException(f"{self.component_type} is supposed to be digits only.")

        if self.score < self.declaration.get('threshold', 0):
            logging.warning(f"{self.component_type} did not reach the threshold set in its declaration.")
            raise ComponentThresholdNotReached(
                f"{self.component_type} did not reach the threshold set in its declaration.")

    def format(self) -> str:
        """
        Format the address component into a string.

        :return: A string representing the address component.
        """
        # TODO: Implement formatting logic
        # Example formatting:
        return self.value
