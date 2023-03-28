import math
import re
from pprint import pprint

import langdetect
from .address_parser_helpers import AddressParserHelperClass
from typing import List
from .address_component import AddressComponent, AddressComponentType
from .exceptions import AddressTokenizationException, ComponentEvaluationException, MissingAddressComponentEvaluation, \
    InconclusiveEvaluationException


class AddressParser:
    def __init__(self, ml: bool = False):
        if ml:
            from .ml_address_parser import MLAddressParser
            self.ml = MLAddressParser()
        else:
            self.ml = None

    def parse_address(self, input_address: str) -> List[AddressComponent]:
        normalized_address = self.normalize_address(input_address)
        try:
            # Tokenize the input address string into individual words
            splits = normalized_address.split()
            words = {w: int(splits.index(w)) for w in splits}

            original_list_size = len(words)
            for i in range(original_list_size):
                if (i + 1) < original_list_size:
                    comb = list(words.keys())[i:i+2]
                    new_string = " ".join(comb)
                    words[new_string] = i

        except AttributeError as e:
            raise AddressTokenizationException

        if self.ml:
            return self.ml.parse_address(input_address)
        else:
            return self.create_address_components(words, input_address)

    def normalize_address(self, input_address: str) -> str:
        # Remove any special characters
        normalized_address = re.sub('[^\w\d\s-]+', '', input_address)

        # Replace abbreviations with their full forms
        abbreviation_map = {
            'st': 'street',
            'ave': 'avenue',
            'rd': 'road',
            'blvd': 'boulevard',
            'hwy': 'highway',
            'ln': 'lane',
            'pkwy': 'parkway',
            'pl': 'place',
            'dr': 'drive',
            'v.': 'vägen',
            'g.': 'gatan'
        }

        for abbreviation, full_form in abbreviation_map.items():
            normalized_address = re.sub(fr'\b{abbreviation}\b', full_form, normalized_address, flags=re.IGNORECASE)

        return normalized_address

    def detect_language(self, input_address: str) -> str:
        """
        Detect the language of the input address using language detection techniques.
        """
        return langdetect.detect(input_address)

    def create_address_components(self, components: dict, input_address: str) -> List[AddressComponent]:
        address_components = []
        # {component_type: {component: (is_type, confidence)}}
        evaluated_components = {}

        for component in components.keys():

            for component_type in AddressComponentType:
                if component_type not in evaluated_components.keys():
                    evaluated_components[component_type] = {}
                try:
                    function = getattr(AddressParserHelperClass, f'is_{component_type.name.lower()}')
                except Exception as e:
                    raise MissingAddressComponentEvaluation(
                        f'There is no function called "is_{component_type.name.lower()}"'
                    ) from e

                try:
                    evaluated_components[component_type][component] = function(component, components.get(component))
                except InconclusiveEvaluationException as e:
                    print(f"Can't say if {component} is a {component_type}")

        for component_type, item in evaluated_components.items():
            for component_value, valuation in item.items():
                try:
                    if valuation[0]:
                        address_components.append(
                            AddressComponent(
                                component_type=component_type,
                                component_value=component_value,
                                position=components.get(component_value),
                                confidence=round(float(valuation[1]), 2)
                            )
                        )
                except TypeError as e:
                    raise ComponentEvaluationException from e
        return self.resolve_conflicts(input_address=input_address, components=address_components)

    def resolve_conflicts(self, input_address: str, components: List[AddressComponent]) -> List[AddressComponent]:
        # sort components by position
        sorted_components = components
        sorted_components.sort(reverse=True)
        resolved_components: List[AddressComponent] = []

        for s_component in sorted_components:
            if s_component.component_type not in set(r.component_type for r in resolved_components):
                resolved_components.append(s_component)

        return resolved_components

    def generate_possible_addresses(self, components: List[AddressComponent]) -> List[str]:
        # Create a list of all possible values for each component type
        values_by_type = {}
        for component in components:
            if component.component_type in values_by_type:
                values_by_type[component.component_type].append(component.component_value)
            else:
                values_by_type[component.component_type] = [component.component_value]

        # Recursively concatenate each value for each component type in all possible combinations
        addresses = []
        self._generate_possible_addresses_helper(values_by_type, '', addresses)
        return addresses

    def _generate_possible_addresses_helper(self, values_by_type, current_address, addresses):
        # Base case: if there are no more component types to process, add the current address to the list of possible
        # addresses
        if not values_by_type:
            addresses.append(current_address.strip())
        else:
            # Recursive case: concatenate each value for the next component type with the current address,
            # and call the function recursively
            next_type = list(values_by_type.keys())[0]
            next_values = values_by_type.pop(next_type)
            for value in next_values:
                self._generate_possible_addresses_helper(values_by_type, f'{current_address} {value}', addresses)
            values_by_type[next_type] = next_values

    def rank_possible_addresses(self, addresses: List[str]) -> List[str]:
        """
        Ranks a list of possible addresses based on their likelihood of being the correct address.

        Args:
        - addresses (List[str]): A list of possible addresses.

        Returns:
        - ranked_addresses (List[str]): A list of the same addresses, ranked by their likelihood of being correct.
        """

        # Define a scoring function for each address
        def score_address(address):
            # Split the input address into components
            input_components = self.parse_address(address)

            # Count the number of matching components between the input address and the possible address
            matching_components = sum(component in address for component in input_components)

            # Compute the average distance between matching components
            distances = []
            for input_component in input_components:
                for possible_component in self.parse_address(address):
                    if input_component.component_type == possible_component.component_type:
                        distances.append(abs(input_component.position - possible_component.position))
            avg_distance = sum(distances) / len(distances)

            # Compute the score as a weighted sum of the number of matching components and the average distance
            score = matching_components + (1 / avg_distance)
            return score

        # Rank the addresses based on their score
        ranked_addresses = sorted(addresses, key=score_address, reverse=True)

        return ranked_addresses
