import unittest
from selectivejsonparser.pattern.pattern_parser import PatternParser
from selectivejsonparser.pattern.element import Element, Dictionary, Array, Value

class TestPattern(unittest.TestCase):
    def test_single_key(self):
        pattern: str = "key"
        parser: PatternParser = PatternParser(pattern)
        result: Element = parser.parse()
        self.assertIsInstance(result, Dictionary)
        self.assertIn("key", result)
        self.assertIsInstance(result["key"], Value)

    def test_nested_keys(self):
        pattern: str = "key1.key2"
        parser: PatternParser = PatternParser(pattern)
        result: Element = parser.parse()
        self.assertIsInstance(result, Dictionary)
        self.assertIn("key1", result)
        self.assertIsInstance(result["key1"], Dictionary)
        self.assertIn("key2", result["key1"])
        self.assertIsInstance(result["key1"]["key2"], Value)
