import json
import logging
from pathlib import Path
from typing import Optional, List

from v2.config import ROOT_PATH
from v2.exceptions import FailedToSaveRuleException, EmptyListException


class Parser:
    """
    A class that represents a rule in a JSON file.

    Attributes:
    - name (str): The name of the rule.
    - flags (list[str]): A list of flags labels that can be used to identify the rule.
    - criteria (list[dict]): A list of criteria that define the rule.

    Methods:
    - load(cls, name: Optional[str] = None, rfilter: Optional[tuple] = None) -> List['Parser']:
      Loads rules from a JSON file, creates a list of Parser objects and returns it. If 'name' is
      provided, filters and returns only the rule with that name. If 'rfilter' is provided,
      filters and returns only the rules that match the flags labels in the filter.

    - to_dict(self) -> dict:
      Returns a dictionary representation of the Rule object.

    - add(self) -> None:
      Adds the current Rule object to the list of rules in the JSON file.

    - delete(self) -> None:
      Deletes the current Rule object from the list of rules in the JSON file.

    - validate_dict(cls, rules: [List[dict], dict]) -> None:
      Validates a list of rules to ensure that each rule is of the correct format.

    - save(cls, rules: [List["Parser"], List[dict]]) -> None:
      Saves a list of Rule objects or dictionaries to the JSON file.
    """
    PATH_TO_RULES = Path(f'{ROOT_PATH}/rule/rules.json')

    def __init__(self, name: str, flags: List[str], criteria: List[dict]) -> None:
        """
        Initializes a new Parser object with the given name, description, flags, and criteria.
        """
        if name is None or flags is None or criteria is None:
            raise ValueError(f'name, flags, and criteria needs to be set.')
        elif len(criteria) == 0:
            raise ValueError(f'There needs to be at least one criteria in a rule.')

        self.log = logging.getLogger(__name__)
        self.name = name
        self.flags = flags
        self.criteria = criteria

    def to_dict(self):
        """
        Returns a dictionary representation of the Parser object.

        Returns:
        - A dictionary representing the Parser object, with keys 'name', 'flags', and 'criteria',
          and their respective values.
        """
        self.log.trace(f'Returning a dictionary representation of the the Rule.')
        return {
            'name': self.name,
            'flags': self.flags,
            'criteria': self.criteria,
        }

    def add(self):
        self.log.trace(f'Adding this Rule to list.')
        existing_rules = self.load()

        if self.name not in [er['name'] for er in existing_rules]:
            existing_rules.append(self.to_dict())

        self.save(existing_rules)

    def delete(self):
        rules = self.load()
        self.log.trace(f'deleting this Rule.')

        for i, rule in enumerate(rules):
            if rule['name'] == self.name:
                rules.pop(i)
                break

        self.save(rules)

    @classmethod
    def load(cls, name: Optional[str] = None, rfilter: Optional[List[str]] = None) -> List[dict]:
        """
        Loads rules from a JSON file, creates a list of Parser objects and returns it. If 'name' is
        provided, filters and returns only the rule with that name. If 'rfilter' is provided,
        filters and returns only the rules that match the flags labels in the filter.

        Args:
        - name (Optional[str]): The name of the rule to filter by.
        - rfilter (Optional[Tuple[str]]): A tuple of flags labels to filter by.

        Returns:
        - A list of Parser objects that match the filter.
        """
        with open(cls.PATH_TO_RULES, 'r') as f:
            rules = json.load(f)

        if name is not None:
            return [r for r in rules if r['name'] == name]

        if rfilter is not None:
            filtered_rules = []
            for rule in rules:
                for f in rfilter:
                    if f in rule['flags']:
                        filtered_rules.append(rule)
                        break

            return filtered_rules

        return rules

    @classmethod
    def save(cls, rules: [List["Parser"], List[dict]]) -> None:
        try:
            if len(rules) == 0:
                raise EmptyListException(f'There was no rules to save. List was empty.')
            if isinstance(rules[0], Parser):
                rules = [r.to_dict() for r in rules]
            elif not isinstance(rules[0], dict):
                raise TypeError(f'"{rules[0]}" is not an instance of "dict" or "Parser"')

            cls.validate_dict(rules)

            with open(cls.PATH_TO_RULES, 'w') as f:
                json.dump(rules, fp=f, indent=4)
        except AssertionError as ae:
            raise FailedToSaveRuleException(f'Invalid rule') from ae
        except EmptyListException as e:
            raise FailedToSaveRuleException(f'The list was empty') from e
        except TypeError as te:
            raise FailedToSaveRuleException(f'At least one rule was not of the correct type. It needs to be an '
                                            f'instance of dict or Parser. Got {type(rules[0])}') from te

    @classmethod
    def validate_dict(cls, rules: [List[dict], dict]):
        if isinstance(rules, dict):
            rules = [rules]

        for rule in rules:
            assert list(rule.keys()) == ['name', 'flags', 'criteria']
