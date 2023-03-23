from typing import List, Optional
import logging

from src.exceptions import BuacheException
from src.rule import Rule
from src.declarations import Declaration


class AddressException(BuacheException):
    pass


class ComponentException(AddressException):
    pass


class ComponentNotFound(ComponentException):
    pass


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


class Address:
    def __init__(self, components: Optional[List[AddressComponent]]):
        """
        A class representing an address, composed of multiple address components.

        :param components: A list of AddressComponent objects representing the components of the address.
        """
        self.components = components or []

    @staticmethod
    def _score_component(substring: str, component_type: str, component_declaration: dict) -> int:
        """
        Given a substring, component type, and component declaration, score the substring based on how well it matches
        the patterns in the declaration.

        :param substring: The substring to score.
        :param component_type: The type of component the substring represents.
        :param component_declaration: The declaration for the component type.
        :return: An integer score representing how well the substring matches the declaration.
        """
        # TODO: Implement scoring logic
        # Example scoring:
        score = 0
        for pattern in component_declaration["patterns"]:
            if pattern in substring:
                score += 1
        return score

    def parse_address(self, address_str: str):
        """
        Parse an address string into its components.

        :param address_str: The address string to parse.
        """
        # Create an empty list to hold the parsed components
        parsed_components = []

        # Iterate over each component type and its declaration
        for component_type, component_declaration in Declaration.read("address_component").items():

            # Create an empty list to hold scores for each substring
            scores = []

            # Iterate over each substring in the address string
            for i in range(len(address_str)):
                for j in range(i, len(address_str)):
                    substring = address_str[i:j + 1]

                    # Score the substring based on how well it matches the component declaration
                    score = self._score_component(substring, component_type, component_declaration)
                    if score > 0:
                        scores.append((substring, score))

            if scores:
                # Sort the scores in descending order
                scores.sort(key=lambda x: x[1], reverse=True)

                # Check if the highest-scoring substring has a score that is greater than or equal to the score of
                # the next highest-scoring substring. If not, then there is ambiguity, and we cannot determine the
                # correct value.
                if scores[0][1] >= scores[1][1]:
                    # The highest-scoring substring is unambiguous, so add it to the list of parsed components
                    value = scores[0][0]
                    component = AddressComponent(value, component_type)
                    parsed_components.append(component)
                else:
                    # There is ambiguity, so we cannot determine the correct value. Log a warning and move on.
                    logging.warning(f"Ambiguous value for {component_type}: {scores[0][0]} or {scores[1][0]}")

        self.components = parsed_components

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

    def __str__(self) -> str:
        """
        Get a formatted version of the address.

        :return: A string representing the formatted address.
        """
        if all(self.components):
            return ' '.join([component.format() for component in self.components])
        else:
            return ''
