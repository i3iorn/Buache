from typing import List, Optional
import logging

from src import BuacheException
from src.rule import Rule


class AddressComponent:
    ALLOWED_LEVELS = {
        'Continent': 0,
        'Country': 1,
        'Region': 2,
        'Sub-region': 3,
        'Administrative Region': 3,
        'Municipality': 4,
        'County': 4,
        'City': 5,
        'Borough': 6,
        'Zip': 6,
        'Street': 7,
        'Street number': 8,
        'Entrance': 9,
        'Apartment number': 10,
    }

    def __init__(
        self, value: str,
        component_type: str = None,
        level: str = None,
        formatted: Optional[str] = None,
        rules: Optional[List[Rule]] = None
    ):
        """
        A class representing a component of an address, such as the street, city, or postal code.

        :param component_type: The type of the address component, such as 'street', 'city', or 'postal_code'.
        :param value: The value of the address component, such as '123 Main St' or 'New York'.
        :param level: The level of the address component, with higher levels representing more general components.
                      Must be one of the values in ALLOWED_LEVELS.
        :param formatted: An optional formatted version of the address component, such as '123 Main St, New York'.
        """

        if component_type not in self.ALLOWED_LEVELS.keys() and component_type is not None:
            raise ValueError(f"Invalid component_type: {component_type}. Allowed types: {self.ALLOWED_LEVELS.keys()}")

        if level not in self.ALLOWED_LEVELS.values() and level is not None:
            raise ValueError(f"Invalid level: {level}. Allowed levels: {self.ALLOWED_LEVELS.values()}")

        self.component_type = component_type \
                              or [k for k, v in self.ALLOWED_LEVELS.items() if v == level][0] \
                              or ValueError(f'Both component_type and level cannot be None at the same time.')

        self.value = value
        self.level = self.ALLOWED_LEVELS[self.component_type]

        self.formatted = formatted

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


class AddressException(BuacheException):
    pass


class ComponentException(AddressException):
    pass


class ComponentNotFound(ComponentException):
    pass


class Address:
    def __init__(self, components: List[AddressComponent]):
        """
        A class representing an address, composed of multiple address components.

        :param components: A list of AddressComponent objects representing the components of the address.
        """
        self.components = components

    def validate(self) -> bool:
        """
        Validate that the address has valid data.

        :return: True if the address is valid, False otherwise.
        """
        # TODO: Implement validation logic
        # Example validation:
        if len(self.components) == 0:
            logging.warning("The address has no components.")
            return False
        for component in self.components:
            if not component.validate():
                logging.warning(f"Invalid component: {component.component_type}")
                return False
        return True

    def get_component(self, component_type: str) -> Optional[AddressComponent]:
        """
        Get the first address component with the given type.

        :param component_type: The type of the address component to get.
        :return: An AddressComponent object if found, or None otherwise.
        """
        for component in self.components:
            if component.component_type == component_type:
                return component
        raise ComponentNotFound(component_type)

    def get_components_by_level(self, level: int) -> List[AddressComponent]:
        """
        Get a list of all address components with the given level.

        :param level: The level of the address components to get.
        :return: A list of AddressComponent objects with the given level.
        """
        # TODO: Add error handling for when level is not found
        return [component for component in self.components if component.level == level]

    def get_formatted_address(self) -> str:
        """
        Get a formatted version of the address.

        :return: A string representing the formatted address.
        """
        # TODO: Handle case when formatted_address is None
        return ' '.join([component.formatted for component in self.components])
