import logging
import re
from typing import List, Tuple

import src.address.helpers
from config import CONFIG
from src.exceptions import MissingAddressComponentEvaluation, InconclusiveEvaluationException, AddressComponentException
from .component import AddressComponentType, AddressComponent


class AddressParser:
    """
    The AddressParser class is responsible for parsing an input address string into a list of AddressComponent objects.

    It contains methods to normalize the address by replacing abbreviations with their full forms, creating tokens to
    split the address into individual components, and evaluating each component to determine its type (e.g. street name,
    city, state, etc.) and confidence level.

    The class also contains helper methods to create AddressComponent objects and to handle exceptions that may occur
    during the evaluation process.

    Overall, the AddressParser class provides a comprehensive solution for parsing and standardizing input addresses,
    making it easier to analyze and process this type of data.
    """

    def __init__(self):
        """
        Constructor for the AddressParser class. Initializes a logger instance for logging purposes.
        """

        self.log = logging.getLogger(__name__)

    def parse_address(self, input_address: str) -> List[AddressComponent]:
        """
        Parses an input address string and returns a list of AddressComponent objects.

        :param input_address: A string representing the input address to be parsed.
        :return: A list of AddressComponent objects.
        """

        normalized_address = self.normalize_address(input_address)
        tokens = self.create_tokens(normalized_address)
        address_components = self.create_address_components(tokens, normalized_address)

        return address_components

    def normalize_address(self, input_address: str) -> str:
        """
        Normalizes an input address string by replacing abbreviations with their full forms.

        :param input_address: A string representing the input address to be normalized.
        :return: A string representing the normalized address.
        """

        abbreviation_map = {option: CONFIG.get('Abbreviations', option) for option in CONFIG.options('Abbreviations')}
        normalized_address = input_address
        for full_form, abbreviation in abbreviation_map.items():
            normalized_address = re.sub(fr'\b{abbreviation}\b', full_form, normalized_address, flags=re.IGNORECASE)
        self.log.debug(f'Normalized address is "{normalized_address}"')
        return normalized_address

    def create_tokens(self, input_address: str) -> dict:
        """
        Creates tokens from an input address string for splitting the address into individual components.

        :param input_address: A string representing the input address to be tokenized.
        :return: A dictionary representing the tokens generated from the input address.
        """

        words = {}
        splits = input_address.split()
        for w in splits:
            words[w] = int(splits.index(w))
        original_list_size = len(words)
        for i in range(original_list_size):
            if (i + 1) < original_list_size:
                comb = list(words.keys())[i:i + 2]
                new_string = " ".join(comb)
                words[new_string] = i
        return words

    def create_address_components(self, tokens: dict, input_address: str) -> List[AddressComponent]:
        """
        Creates a list of AddressComponent objects by evaluating each token generated from the input address.

        :param tokens: A dictionary representing the tokens generated from the input address.
        :param input_address: A string representing the input address to be parsed.
        :return: A list of AddressComponent objects.
        """

        # Any component with a lower confidence than this is discarded.
        threshhold = float(CONFIG.get('AddressHeuristics.evaluation', 'threshold'))

        evaluated_components = self.evaluate_address_components(tokens, input_address)
        address_components = []
        for component_type, components in evaluated_components.items():
            for component_value, valuation in components.items():
                if valuation[0] and valuation[1] > threshhold:
                    component = self.create_address_component(component_type, component_value, tokens, valuation)
                    address_components.append(component)
        return address_components

    def create_address_component(self, component_type: AddressComponentType, component_value: str, tokens: dict,
                                 valuation: Tuple) -> AddressComponent:
        """
        Creates an AddressComponent object based on the provided component type, value, and valuation.

        :param component_type: An AddressComponentType object representing the type of the address component.
        :param component_value: A string representing the value of the address component.
        :param tokens: A dictionary representing the tokens generated from the input address.
        :param valuation: A tuple representing the valuation of the address component.
        :return: An AddressComponent object.
        """

        position = tokens[component_value]
        confidence = round(float(valuation[1]), 2)
        return AddressComponent(
            component_type=component_type,
            component_value=component_value,
            position=position,
            confidence=confidence
        )

    def evaluate_address_components(self, components: dict, input_address: str) -> dict:
        """
        Evaluates each token generated from the input address to determine its type and confidence level.

        :param components: A dictionary representing the tokens generated from the input address.
        :param input_address: A string representing the input address to be parsed.
        :return: A dictionary representing the evaluated components with their corresponding types and confidence levels.
        """

        evaluated_components = {}
        for component in components.keys():
            for component_type in AddressComponentType:
                if component_type not in evaluated_components.keys():
                    evaluated_components[component_type] = {}
                evaluated_components[component_type][component] = self.evaluate_address_component(
                    component=component,
                    input_address=input_address,
                    component_type=component_type,
                    position=components.get(component)
                )

        return evaluated_components

    def evaluate_address_component(
            self,
            component: str = None,
            position: int = None,
            input_address: str = None,
            component_type: AddressComponentType = None
    ) -> Tuple:
        """
        Evaluates a single address component token to determine its type and confidence level.

        :param component_type:
        :param input_address:
        :param component: A string representing the address component token to be evaluated.
        :param position: An integer representing

        :return: A tuple with the result and a confidence score.
        """

        # Get the evaluation function dynamically based on the component type
        func_name = f'is_{component_type.name.lower()}'
        evaluation_func = getattr(src.address.helpers, func_name, None)

        if evaluation_func is None:
            raise MissingAddressComponentEvaluation(f'There is no function called "{func_name}"')

        # Evaluate the component
        try:
            self.log.debug(f'Adding tests to check if "{component}" is a "{component_type.name.lower()}"')
            return evaluation_func(
                token=component,
                position=position,
                full_address=input_address
            )
        except InconclusiveEvaluationException:
            self.log.debug(f"Can't say if {component} is a {component_type}")
            return False, 0
