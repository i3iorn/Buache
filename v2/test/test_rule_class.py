import operator
from typing import Any

from v2 import Rule
from unittest import TestCase


class TestRule(TestCase):
    def test_asserts_is(self):
        r = Rule()
        values = [1, 1]
        self.assertTrue(r.asserts('is', values))

    def test_asserts_gt(self):
        r = Rule()
        values = [2, 1]
        self.assertTrue(r.asserts('gt', values))

    def test_evaluate(self):
        r = Rule()
        self.assertIsNone(r.evaluate())
