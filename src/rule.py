import re


class Rule:
    """
    A class to define a parsing rule.
    """

    def __init__(self, name, pattern=None, index=None, min_length=None, max_length=None,
                 dependencies=None, allowed_values=None, min_value=None, max_value=None,
                 disallowed_substrings=None, custom_match_function=None):
        """
        Constructor method.
        :param name: the name of the parsed address part
        :param pattern: a regex pattern for matching the address part
        :param index: the index of the address line containing the parsed part
        :param min_length: the minimum length of the address part
        :param max_length: the maximum length of the address part
        :param dependencies: a list of other address parts that this part depends on
        """
        self.name = name
        self.pattern = pattern
        self.index = index
        self.min_length = min_length
        self.max_length = max_length
        self.dependencies = dependencies or []
        self.allowed_values = allowed_values or []
        self.min_value = min_value
        self.max_value = max_value
        self.disallowed_substrings = disallowed_substrings or []
        self.custom_match_function = custom_match_function

    def matches(self, address, parts):
        """
        Checks if the rule matches the address.
        :param address: the address to be matched
        :param parts: a dictionary containing previously identified address parts
        :return: True if the rule matches, False otherwise
        """
        if self.pattern:
            match = re.search(self.pattern, address, re.IGNORECASE)
            if not match:
                return False

        if self.index is not None:
            address_lines = address.split(", ")
            if self.index < 0 or self.index >= len(address_lines):
                return False

        if self.min_length is not None:
            if len(parts.get(self.name, "")) < self.min_length:
                return False

        if self.max_length is not None:
            if len(parts.get(self.name, "")) > self.max_length:
                return False

        for dependency in self.dependencies:
            if not parts.get(dependency, ""):
                return False

        if self.min_value is not None and address < self.min_value:
            return False

        if self.max_value is not None and address > self.max_value:
            return False

        if any(substring in address for substring in self.disallowed_substrings):
            return False

        if self.custom_match_function and not self.custom_match_function(address):
            return False

        return True

"""
import re

class Rule:
    def __init__(self, condition, action):
        self.condition = condition
        self.action = action
    
    def evaluate(self, fact):
        if self.condition(fact):
            return self.action(fact)

class RuleEngine:
    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def execute(self, fact):
        for rule in self.rules:
            result = rule.evaluate(fact)
            if result:
                return result

"""