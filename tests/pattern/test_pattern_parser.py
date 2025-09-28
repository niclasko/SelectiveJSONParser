import unittest
from selectivejsonparser.pattern import PatternParser
from selectivejsonparser.pattern.element import Element, Dictionary, Array, Value
from typing import List

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

    def test_array_of_keys(self):
        pattern: str = "[key]"
        parser: PatternParser = PatternParser(pattern)
        result: Element = parser.parse()
        self.assertIsInstance(result, Array)
        self.assertIsInstance(result[0], Dictionary)
        self.assertIn("key", result[0])
        self.assertIsInstance(result[0]["key"], Value)
    
    def test_complex_pattern(self):
        pattern: str = "key1.key2[(key3|key4).key5]"
        parser: PatternParser = PatternParser(pattern)
        result: Element = parser.parse()
        self.assertIsInstance(result, Dictionary)
        self.assertIn("key1", result)
        self.assertIsInstance(result["key1"], Dictionary)
        self.assertIn("key2", result["key1"])
        self.assertIsInstance(result["key1"]["key2"], Array)
        array: Element = result["key1"]["key2"]
        self.assertIsInstance(array[0], Dictionary)

        self.assertIn("key3", array[0])
        self.assertIsInstance(array[0]["key3"], Dictionary)
        self.assertIn("key4", array[0])

        self.assertIsInstance(array[0]["key4"], Dictionary)
        self.assertIn("key5", array[0]["key4"])
        self.assertIsInstance(array[0]["key4"]["key5"], Value)

        self.assertIsInstance(array[0]["key3"], Dictionary)
        self.assertIn("key5", array[0]["key3"])
        self.assertIsInstance(array[0]["key3"]["key5"], Value)
        

if __name__ == "__main__":
    unittest.main()