import unittest
from pprint import pprint

from v2.rule import Rule
from v2.test import TestRule, TestParser

rule = Rule('street_name')
pprint(rule.evaluate('Danagränd 7 17566 Järfälla'))

unittest.main()
