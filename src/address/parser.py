import configparser
import logging
import os
import re
from pathlib import Path

import langdetect
from .helpers import AddressParserHelperClass
from typing import List
from src.address.component import AddressComponent, AddressComponentType
from src.exceptions import AddressTokenizationException, ComponentEvaluationException, \
    MissingAddressComponentEvaluation, \
    InconclusiveEvaluationException, NormalizationError


class AddressParser:
    def __init__(self, country: configparser.ConfigParser):
        self.log = logging.getLogger(__name__)

        self.country = country
        self.log.debug(f'Country is set to: {country}')

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

        try:
            normalized_address = self.normalize_address(input_address)
        except NormalizationError as e:
            self.log.warning(f'Failed to normalize address.')
            normalized_address = input_address

        return self.create_address_components(words, normalized_address)

    def normalize_address(self, input_address: str) -> str:
        # Remove any special characters
        normalized_address = re.sub('[^\w\d\s\-\:]+', '', input_address)

        abbreviation_map = {}

        if self.country.has_section('Abbreviations'):
            for option in self.country.options('Abbreviations'):
                abbreviation_map[option] = self.country.get('Abbreviations', option)

        for full_form, abbreviation in abbreviation_map.items():
            normalized_address = re.sub(fr'\b{abbreviation}\b', full_form, normalized_address, flags=re.IGNORECASE)

        return normalized_address

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
                    self.log.debugx(f'Adding tests to check if "{component}" is a "{component_type.name.lower()}"')
                    evaluated_components[component_type][component] = function(
                        self=AddressParserHelperClass,
                        token=component,
                        position=components.get(component),
                        full_address=input_address
                    )
                except InconclusiveEvaluationException as e:
                    self.log.debug(f"Can't say if {component} is a {component_type}")

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
        return self.resolve_conflicts(components=address_components)

    def resolve_conflicts(self, components: List[AddressComponent]) -> List[AddressComponent]:
        # sort components by position
        sorted_components = components
        sorted_components.sort(reverse=True)
        resolved_components: List[AddressComponent] = []

        for s_component in sorted_components:
            if s_component.component_type not in set(r.component_type for r in resolved_components):
                resolved_components.append(s_component)

        return resolved_components
