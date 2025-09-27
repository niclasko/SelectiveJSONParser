import unittest
from selectivejsonparser.pattern import Pattern

class TestPattern(unittest.TestCase):
    def test_single_key(self):
        pattern: Pattern = Pattern("key")
        self.assertTrue(pattern.match("key"))

    def test_multiple_keys(self):
        pattern: Pattern = Pattern("key1.key2")
        self.assertTrue(pattern.match("key1"))
        self.assertTrue(pattern.match("key2"))

    def test_array_index(self):
        pattern: Pattern = Pattern("key1[].key2")
        self.assertTrue(pattern.match("key1"))
        self.assertTrue(pattern.match(0))
        self.assertTrue(pattern.match("key2"))

    def test_key_with_or(self):
        pattern: Pattern = Pattern("key1|key2")
        self.assertTrue(pattern.match("key1"))
        pattern.previous()  # Move back to test the second key
        self.assertTrue(pattern.match("key2"))