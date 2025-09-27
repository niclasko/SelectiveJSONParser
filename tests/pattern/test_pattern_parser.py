import unittest
from selectivejsonparser.pattern import PatternParser
from selectivejsonparser.pattern.element import Element, Key, Index, Anything
from typing import List

class TestPattern(unittest.TestCase):
    def test_single_key(self):
        pattern = PatternParser("key")
        elements: List[Element] = list(pattern.parse())
        self.assertEqual(len(elements), 2)
        self.assertIsInstance(elements[0], Key)
        self.assertIn("key", elements[0])
        self.assertIsInstance(elements[1], Anything)

    def test_multiple_keys(self):
        pattern = PatternParser("key1.key2")
        elements: List[Element] = list(pattern.parse())
        self.assertEqual(len(elements), 3)
        self.assertIsInstance(elements[0], Key)
        self.assertIn("key1", elements[0])
        self.assertIsInstance(elements[1], Key)
        self.assertIn("key2", elements[1])
        self.assertIsInstance(elements[2], Anything)

    def test_key_with_or(self):
        pattern = PatternParser("key1|key2")
        elements: List[Element] = list(pattern.parse())
        self.assertEqual(len(elements), 2)
        self.assertIsInstance(elements[0], Key)
        self.assertIn("key1", elements[0])
        self.assertIn("key2", elements[0])
        self.assertIsInstance(elements[1], Anything)

    def test_key_with_wildcard(self):
        pattern = PatternParser("*")
        elements: List[Element] = list(pattern.parse())
        self.assertEqual(len(elements), 2)
        self.assertIsInstance(elements[0], Key)
        self.assertIn("*", elements[0])
        self.assertIsInstance(elements[1], Anything)

    def test_key_and_index(self):
        pattern = PatternParser("key1[].key2")
        elements: List[Element] = list(pattern.parse())
        self.assertEqual(len(elements), 4)
        self.assertIsInstance(elements[0], Key)
        self.assertIn("key1", elements[0])
        self.assertIsInstance(elements[1], Index)
        self.assertIsInstance(elements[2], Key)
        self.assertIn("key2", elements[2])
        self.assertIsInstance(elements[3], Anything)

    def test_index_and_key(self):
        pattern = PatternParser("[].key1")
        elements: List[Element] = list(pattern.parse())
        self.assertEqual(len(elements), 3)
        self.assertIsInstance(elements[0], Index)
        self.assertIsInstance(elements[1], Key)
        self.assertIn("key1", elements[1])
        self.assertIsInstance(elements[2], Anything)

    def test_complex_pattern(self):
        pattern = PatternParser("[].key1|key2.key3")
        elements: List[Element] = list(pattern.parse())
        self.assertEqual(len(elements), 4)
        self.assertIsInstance(elements[0], Index)
        self.assertIsInstance(elements[1], Key)
        self.assertIn("key1", elements[1])
        self.assertIn("key2", elements[1])
        self.assertIsInstance(elements[2], Key)
        self.assertIn("key3", elements[2])
        self.assertIsInstance(elements[3], Anything)

if __name__ == "__main__":
    unittest.main()