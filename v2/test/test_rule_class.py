import json
from pathlib import Path
from unittest import TestCase

from v2.config import ROOT_PATH
from v2.rule import Rule
from v2.rule.parser import Parser


class TestRule(TestCase):
    PATH_TO_TEST_RULES = Path(f'{ROOT_PATH}/rule/test_rules.json')

    def setUp(self):
        # create a test rules file
        with open(self.PATH_TO_TEST_RULES, 'w') as f:
            json.dump([], f)
        Parser.PATH_TO_RULES = self.PATH_TO_TEST_RULES
        parser = Parser('base_test_rule', ['base_test_flag'], [{
            "type": "string_type",
            "required": True,
            "string_type": "isalpha",
        }])
        parser.min = 2
        parser.max = 40
        parser.add()

    def tearDown(self):
        # remove the test rules file
        # remove the test rules file
        try:
            self.PATH_TO_TEST_RULES.unlink(missing_ok=True)
        except FileNotFoundError:
            pass

    def test_asserts_is(self):
        r = Rule('test_rule')
        values = [1, 1]
        self.assertTrue(r.asserts('is', values))

    def test_asserts_gt(self):
        r = Rule('test_rule')
        values = [2, 1]
        self.assertTrue(r.asserts('gt', values))

    def test_init_with_no_name(self):
        with self.assertRaises(ValueError):
            Rule()

    def test_init_with_name(self):
        r = Rule('test_rule')
        self.assertEqual(r.name, 'test_rule')

    def test_exists_when_rule_exists(self):
        r = Rule('base_test_rule')
        self.assertTrue(r.saved())

    def test_exists_when_rule_does_not_exist(self):
        r = Rule('non_existent_rule')
        self.assertFalse(r.saved())

    def test_asserts_with_invalid_assertion_type(self):
        r = Rule('test_rule')
        values = [1, 1]
        with self.assertRaises(KeyError):
            r.asserts('invalid_assert_type', values)

    def test_asserts_with_invalid_number_of_values(self):
        r = Rule('test_rule')
        values = [1]
        with self.assertRaises(TypeError):
            r.asserts('is', values)

    def test_asserts_is_with_false_result(self):
        r = Rule('test_rule')
        values = [1, 2]
        with self.assertRaises(AssertionError):
            r.asserts('is', values)

    def test_asserts_gt_with_false_result(self):
        r = Rule('test_rule')
        values = [1, 2]
        with self.assertRaises(AssertionError):
            r.asserts('gt', values)
