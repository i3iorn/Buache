import json
import logging
from pathlib import Path
from typing import Optional, List, Tuple, Any

from v2.config import ROOT_PATH


class Parser:
    """
    A class that represents a rule in a JSON file.

    Attributes:
    - name (str): The name of the rule.
    - description (str): A description of the rule.
    - flags (list[str]): A list of flags labels that can be used to identify the rule.
    - criteria (list[dict]): A list of criteria that define the rule.

    Methods:
    - load(cls, name: Optional[str] = None, rfilter: Optional[tuple] = None) -> List['Parser']:
      Loads rules from a JSON file, creates a list of Parser objects and returns it. If 'name' is
      provided, filters and returns only the rule with that name. If 'rfilter' is provided,
      filters and returns only the rules that match the flags labels in the filter.

    """
    PATH_TO_RULES = Path(f'{ROOT_PATH}/rule/rules.json')

    def __init__(self, name: str, description: str, flags: List[str], criteria: List[dict]) -> None:
        """
        Initializes a new Parser object with the given name, description, flags, and criteria.
        """
        self.log = logging.getLogger(__name__)
        self.name = name
        self.description = description
        self.flags = flags
        self.criteria = criteria

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'flags': self.flags,
            'criteria': self.criteria,
        }

    def add(self):
        rules = self.load()

        rules.append(self.to_dict())

        self.save(rules)

    def delete(self):
        rules = self.load()

        for i, rule in enumerate(rules):
            if rule['name'] == self.name:
                rules.pop(i)
                break

        self.save(rules)

    def save(self, rules: [List["Parser"], List[dict]]) -> None:
        if isinstance(rules[0], dict):
            pass
        elif isinstance(rules[0], Parser):
            rules = [r.to_dict() for r in rules]
        else:
            raise TypeError(f'{rules[0]} is not an instance of "dict" or "Parser"')

        with open(self.PATH_TO_RULES, 'w') as f:
            json.dump(f, rules)

    @classmethod
    def load(cls, name: Optional[str] = None, rfilter: Optional[Tuple[str]] = None) -> List[dict]:
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

        rule_list = [cls(
            name=rule['name'],
            description=rule['description'],
            flags=rule['flags'],
            criteria=rule['criteria'],
        ).to_dict() for rule in rules]

        if name is not None:
            return [r for r in rule_list if r['name'] == name]

        if rfilter is not None:
            filtered_rules = []
            for r in rule_list:
                if set(rfilter).issubset(set(r['flags'])):
                    filtered_rules.append(r)
            return filtered_rules

        return rule_list
