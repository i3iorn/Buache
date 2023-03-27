from unittest import TestCase
import json
from pathlib import Path

from v2.config import ROOT_PATH
from v2.exceptions import FailedToSaveRuleException
from v2.rule.parser import Parser


class TestParser(TestCase):
    PATH_TO_TEST_RULES = Path(f'{ROOT_PATH}/rule/test_rules.json')

    def setUp(self):
        # create a test rules file
        with open(self.PATH_TO_TEST_RULES, 'w') as f:
            json.dump([], f)
        Parser.PATH_TO_RULES = self.PATH_TO_TEST_RULES
        self.criteria = [{"type": "string_type", "required": True, "string_type": "isalpha"}]
        parser = Parser('base_test_rule', ['base_test_flag'], self.criteria)
        parser.add()

    def tearDown(self):
        # remove the test rules file
        # remove the test rules file
        try:
            self.PATH_TO_TEST_RULES.unlink(missing_ok=True)
        except FileNotFoundError:
            pass

    def test_load_with_filter(self):
        # add a rule to the test rules file
        parser1 = Parser('test_rule1', ['test_flag1'], self.criteria)
        parser2 = Parser('test_rule2', ['test_flag2'], self.criteria)
        Parser.save([parser1, parser2])
        # load rules and check if the rule is in the list
        rules = Parser.load(rfilter=['test_flag1'])
        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0]['name'], 'test_rule1')

    def test_load_without_filter(self):
        # add a rule to the test rules file
        parser = Parser('test_rule', ['test_flag'], self.criteria)
        parser.save([parser])
        # load rules and check if the rule is in the list
        rules = Parser.load()
        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0]['name'], 'test_rule')

    def test_add(self):
        # add a rule to the test rules file
        parser = Parser('test_rule', ['test_flag'], self.criteria)
        parser.add()
        # load rules and check if the rule is in the list
        rules = Parser.load()
        self.assertEqual(len(rules), 2)
        self.assertEqual(rules[1]['name'], 'test_rule')

    def test_delete(self):
        # add a rule to the test rules file
        parser = Parser('test_rule', ['test_flag'], self.criteria)
        parser.add()
        # delete the rule from the test rules file
        parser.delete()
        # load rules and check if the rule is not in the list
        rules = Parser.load()
        self.assertEqual(len(rules), 1)

    def test_save_with_parser_instances(self):
        # add a rule to the test rules file
        parser = Parser('test_rule', ['test_flag'], self.criteria)
        Parser.save([parser])
        # load rules and check if the rule is in the list
        rules = Parser.load()
        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0]['name'], 'test_rule')

    def test_save_with_dict_instances(self):
        # add a rule to the test rules file
        rule = {'name': 'test_rule', 'flags': ['test_flag'], 'criteria': self.criteria}
        Parser.save([rule])
        # load rules and check if the rule is in the list
        rules = Parser.load()
        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0]['name'], 'test_rule')

    def test_save_with_invalid_type(self):
        with self.assertRaises(FailedToSaveRuleException):
            Parser.save(['invalid_type'])

    def test_to_dict_with_flags(self):
        parser = Parser('test_rule', ['test_flag1', 'test_flag2'], self.criteria)
        rule_dict = parser.to_dict()
        self.assertEqual(rule_dict['name'], 'test_rule')
        self.assertListEqual(rule_dict['flags'], ['test_flag1', 'test_flag2'])
        self.assertListEqual(rule_dict['criteria'], self.criteria)

    def test_to_dict_with_conditions(self):
        parser = Parser('test_rule', [], self.criteria)
        rule_dict = parser.to_dict()
        self.assertEqual(rule_dict['name'], 'test_rule')
        self.assertListEqual(rule_dict['flags'], [])
        self.assertDictEqual(rule_dict['criteria'][0], self.criteria[0])

    def test_to_dict_with_flags_and_conditions(self):
        parser = Parser('test_rule', ['test_flag'], self.criteria)
        rule_dict = parser.to_dict()
        self.assertEqual(rule_dict['name'], 'test_rule')
        self.assertListEqual(rule_dict['flags'], ['test_flag'])
        self.assertDictEqual(rule_dict['criteria'][0], self.criteria[0])

    def test_load_invalid_path(self):
        Parser.PATH_TO_RULES = 'invalid_path.json'
        with self.assertRaises(FileNotFoundError):
            Parser.load()

    def test_load_invalid_json(self):
        # create a test rules file with invalid JSON
        with open(self.PATH_TO_TEST_RULES, 'w') as f:
            f.write('invalid_json')
        Parser.PATH_TO_RULES = self.PATH_TO_TEST_RULES
        with self.assertRaises(json.JSONDecodeError):
            Parser.load()

    def test_save_invalid_rule(self):
        # create an invalid rule
        invalid_rule = {'name': 'invalid_rule', 'flags': 'invalid_flags'}
        with self.assertRaises(FailedToSaveRuleException):
            Parser.save([invalid_rule])

    def test_invalid_parser_creation(self):
        with self.assertRaises(ValueError):
            Parser(None, ['test_flag'], self.criteria)

    def test_invalid_parser_saving(self):
        with self.assertRaises(TypeError):
            parser = Parser('test_rule', ['test_flag'], self.criteria)
            parser.save(parser)

    def test_invalid_load_path(self):
        with self.assertRaises(FileNotFoundError):
            Parser.PATH_TO_RULES = Path('/path/to/invalid/rules.json')
            Parser.load()
