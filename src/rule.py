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

    def evaluate(self, address, components):
        """
        Checks if the rule matches the address.
        :param address: the address to be matched
        :param components: a list containing previously identified address components
        :return: True if the rule matches, False otherwise
        """

        return True

    @classmethod
    def from_dict(cls, rule):
        pass
