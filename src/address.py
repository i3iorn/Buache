import logging
from typing import List, Optional, TYPE_CHECKING
from src.exceptions import AddressComponentNotFound, MissingRuleDeclarationForComponent, \
    ToManyRulesDeclaredForComponent, AddressComponentException, AmbiguousScoresException
from src.declarations import Declaration

if TYPE_CHECKING:
    from src import AddressComponent, Rule


class Address:
    def __init__(self, components: Optional[List['AddressComponent']] = None):
        """
        A class representing an address, composed of multiple address components.

        :param components: A list of AddressComponent objects representing the components of the address.
        """
        self.components = components or []
        self.log = logging.getLogger(__name__)

    def __str__(self) -> str:
        """
        Get a formatted version of the address.

        :return: A string representing the formatted address.
        """
        self.log.trace('Entering')
        return ' '.join([component.format() for component in self.components])

    def _read_rule(self, component_type: str):
        """
        Read the component declaration and rule for a given component type.

        :param component_type: The component type to read.
        :return: A tuple of the component declaration and rule.
        """
        from src.declarations import Declaration
        from src import Rule

        rule_dict = Declaration.read("rule", component_type)

        if len(rule_dict) == 0:
            raise MissingRuleDeclarationForComponent(f'{component_type} has no rules declared')
        elif len(rule_dict) >= 2:
            raise ToManyRulesDeclaredForComponent(f'Each component can only have one rule declared. '
                                                  f'{component_type} has {len(rule_dict)}')
        else:
            rule = Rule.from_dict(rule_dict[0])
            return rule

    @staticmethod
    def _score_component(
            index: int,
            substring: str,
            rule: 'Rule',
            previously_identified_components: List['AddressComponent']
    ) -> int:
        """
        Given a substring, component type, and component declaration, score the substring based on how well it matches
        the patterns in the declaration.

        :param substring: The substring to score.
        :param rule: Rule applicable for the component.
        :param previously_identified_components: What the name says.

        :return: An integer score representing how well the substring matches the declaration.
        """
        # TODO: Implement scoring logic
        # Example scoring:

        if rule.evaluate(index, substring, previously_identified_components):
            score = 1

        return score

    def parse_address(self, address_str: str):
        """
        Parse an address string into its components.

        :param address_str: The address string to parse.
        """
        self.log.trace('Entering')

        self.log.trace("Create an empty list to hold the parsed components")
        parsed_components = []

        self.log.trace("Iterate over each component type and its declaration")
        for component_declaration in Declaration.read("address_component"):
            component_type = component_declaration.get('name')
            try:
                rule = self._read_rule(component_type)
                self.log.trace(f"Create an empty list to hold scores for each substring")
                scores = []

                lengths = component_declaration.get('length')

                self.log.trace(f"Iterate over each substring in the address string")
                for i in range(len(address_str)):
                    for j in range(i, len(address_str)):
                        if lengths[0] <= j <= lengths[1]:
                            substring = address_str[i:j + 1]

                            # Score the substring based on how well it matches the component declaration
                            self.log.trace(f"Calculate score for '{substring}' against {component_type} rules.")
                            self.log.trace(f"Applicable rules are {rule.criteria}")
                            score = self._score_component(i, component_type, rule, parsed_components)
                            if score > 0:
                                scores.append((substring, score, i))

                        try:
                            if scores:
                                self.log.debug(f'Generated {len(scores)} scores')
                                best_component = self._process_scores(scores, component_type)

                                if best_component is not None:
                                    self.log.debug(f'The best component was considered {best_component.component_type} for "{best_component.value}"')
                                    parsed_components.append(best_component)
                        except AmbiguousScoresException as e:
                            self.log.debug(f'Moving on to next substring since this one gives unclear results.')

            except MissingRuleDeclarationForComponent as e:
                self.log.warning(f'There are no rules declared for {component_type}', exc_info=e)

        self.components = parsed_components

    def get_component(self, component_type: str) -> Optional['AddressComponent']:
        """
        Get the first address component with the given type.

        :param component_type: The type of the address component to get.
        :return: An AddressComponent object if found, or None otherwise.
        """
        self.log.trace('Entering')
        for component in self.components:
            if component.component_type == component_type:
                return component
        raise AddressComponentNotFound(component_type)

    def _process_scores(self, scores, component_type):
        from src import AddressComponent
        # Sort the scores in descending order
        scores.sort(key=lambda x: x[1], reverse=True)

        # Check if the highest-scoring substring has a score that is greater than or equal to the score of
        # the next highest-scoring substring. If not, then there is ambiguity, and we cannot determine the
        # correct value.
        value = None
        if len(scores) == 0:
            value = scores[0][0]
        elif scores[0][1] > scores[1][1]:
            # The highest-scoring substring is unambiguous, so add it to the list of parsed components
            value = scores[0][0]

        if value is not None:
            try:
                return AddressComponent(value=value, component_type=component_type, index=scores[0][2], score=scores[0][1])
            except AddressComponentException as e:
                self.log.debug(f'{value} does not match requirements.', exc_info=e)
                return None
        else:
            # There is ambiguity, so we cannot determine the correct value. Log a warning and move on.
            logging.warning(f"Ambiguous value for {component_type}: {scores[0][0]}({scores[0][1]}) or {scores[1][0]}({scores[0][1]})")
            raise AmbiguousScoresException
