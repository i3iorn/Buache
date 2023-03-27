import unittest

from v2 import AddressComponent, Rule
from v2.test import TestRule, TestParser

components = [AddressComponent('street_number', 11)]
strings = "Danagränd 7 1001 17566 Järfälla".split(" ")
for string in strings:
    for rule_name in Rule.available_rules():
        rule = Rule(rule_name)
        print([string, rule_name, rule.evaluate(string, 0, components)])

unittest.main()
