import unittest

from selectivejsonparser.parser import Parser, json
class TestParser(unittest.TestCase):
    def test_parse_empty_string(self):
        with self.assertRaises(ValueError):
            Parser("").parse()

    def test_parse_simple_dict(self):
        result: json = Parser('{"key": "value"}').parse()
        self.assertEqual(result, {"key": "value"})

    def test_parse_nested_dict(self):
        result: json = Parser('{"outer": {"inner": 42}}').parse()
        self.assertEqual(result, {"outer": {"inner": 42}})

    def test_parse_list(self):
        result: json = Parser('["item1", "item2", 3]').parse()
        self.assertEqual(result, ["item1", "item2", 3])

    def test_parse_boolean(self):
        result: json = Parser('{"isTrue": true, "isFalse": false}').parse()
        self.assertEqual(result, {"isTrue": True, "isFalse": False})

    def test_parse_complex_structure(self):
        text: str = '''
        {
            "name": "Test",
            "age": 30,
            "is_student": false,
            "courses": ["Math", "Science"],
            "address": {"city": "New York", "zip": "10001"},
            "scores": [95.5, 88.0, 76.5]
        }
        '''
        expected: json = {
            "name": "Test",
            "age": 30,
            "is_student": False,
            "courses": ["Math", "Science"],
            "address": {"city": "New York", "zip": "10001"},
            "scores": [95.5, 88.0, 76.5]
        }
        result: json = Parser(text).parse()
        self.assertEqual(result, expected)

    def test_parse_null(self):
        result: json = Parser('{"key": null}').parse()
        self.assertEqual(result, {"key": None})

    def test_parse_number(self):
        result: json = Parser('{"int": 42, "float": 3.14}').parse()
        self.assertEqual(result, {"int": 42, "float": 3.14})

    def test_parse_invalid_json(self):
        with self.assertRaises(ValueError):
            Parser('{"key": "value"').parse()  # Missing closing brace

    def test_parse_unterminated_string(self):
        with self.assertRaises(ValueError):
            Parser('{"key": "value}').parse()  # Unterminated string

    def test_parse_extra_comma(self):
        with self.assertRaises(ValueError):
            Parser('{"key": "value",}').parse()  # Extra comma

    def test_parse_whitespace(self):
        result: json = Parser('  {  "key"  :  "value"  }  ').parse()
        self.assertEqual(result, {"key": "value"})

    def test_parse_empty_dict(self):
        result: json = Parser('{}').parse()
        self.assertEqual(result, {})

    def test_parse_empty_list(self):
        result: json = Parser('[]').parse()
        self.assertEqual(result, [])

    def test_parse_list_of_dicts(self):
        result: json = Parser('[{"key1": "value1"}, {"key2": "value2"}]').parse()
        self.assertEqual(result, [{"key1": "value1"}, {"key2": "value2"}])

    def test_parse_dict_with_various_types(self):
        result: json = Parser('{"str": "text", "num": 123, "bool": true, "null": null, "list": [1, 2], "dict": {"a": 1}}').parse()
        self.assertEqual(result, {
            "str": "text",
            "num": 123,
            "bool": True,
            "null": None,
            "list": [1, 2],
            "dict": {"a": 1}
        })
    
    def test_parse_escaped_characters(self):
        result: json = Parser(r'{"text": "Line1\nLine2\tTabbed\"Quote\""}').parse()
        self.assertEqual(result, {"text": r"Line1\nLine2\tTabbed\"Quote\""})

    def test_parse_unicode_characters(self):
        result: json = Parser(r'{"emoji": "\uD83D\uDE00"}').parse()
        self.assertEqual(result, {"emoji": r"\uD83D\uDE00"})

    def test_parse_large_numbers(self):
        result: json = Parser('{"bigInt": 12345678901234567890, "bigFloat": 1.7976931348623157e+308}').parse()
        self.assertEqual(result, {"bigInt": 12345678901234567890, "bigFloat": 1.7976931348623157e+308})
    
    def test_invalid_number_format(self):
        with self.assertRaises(ValueError):
            Parser('{"invalidNum": 1.7e+}').parse()  # Invalid exponent

    def test_leading_trailing_whitespace(self):
        result: json = Parser('   { "key": "value" }   ').parse()
        self.assertEqual(result, {"key": "value"})

    def test_escaped_key_in_dict(self):
        result: json = Parser(r'{"key\"with\"quotes": "value"}').parse()
        self.assertEqual(result, {r'key\"with\"quotes': "value"})

    def test_with_patterns(self):
        with self.subTest("Pattern matching for specific keys"):
            text: str = '{"name": "Alice", "age": 25, "city": "Wonderland"}'
            pattern: str = "name"
            result: json = Parser(text, pattern).parse()
            self.assertEqual(result, {"name": "Alice"})
        with self.subTest("Pattern matching for nested keys"):
            text: str = '{"user": {"name": "Bob", "details": {"age": 30, "city": "Builderland"}}}'
            pattern: str = "user.details.age"
            result: json = Parser(text, pattern).parse()
            self.assertEqual(result, {"user": {"details": {"age": 30}}})
        with self.subTest("Pattern matching for non-existent keys"):
            text: str = '{"name": "Charlie", "age": 28}'
            pattern: str = "address"
            result: json = Parser(text, pattern).parse()
            self.assertEqual(result, {})
        with self.subTest("Pattern matching with multiple keys"):
            text: str = '{"name": "Diana", "age": 22, "city": "Themyscira", "occupation": "Warrior"}'
            pattern: str = "name|city"
            result: json = Parser(text, pattern).parse()
            self.assertEqual(result, {"name": "Diana", "city": "Themyscira"})
        with self.subTest("Pattern matching in lists of dicts"):
            text: str = '[{"name": "Eve", "age": 29}, {"name": "Frank", "age": 33}]'
            pattern: str = "[name]"
            result: json = Parser(text, pattern).parse()
            self.assertEqual(result, [{"name": "Eve"}, {"name": "Frank"}])
        with self.subTest("Pattern matching in nested lists"):
            text: str = '{"users": [{"name": "Grace", "age": 27}, {"name": "Heidi", "age": 31}]}'
            pattern: str = "users[name]"
            result: json = Parser(text, pattern).parse()
            self.assertEqual(result, {"users": [{"name": "Grace"}, {"name": "Heidi"}]})
        with self.subTest("Pattern matching in deeply nested structures"):
            text: str = '{"company": {"employees": [{"name": "Ivan", "role": "Developer"}, {"name": "Judy", "role": "Manager"}]}}'
            pattern: str = "company.employees[name]"
            result: json = Parser(text, pattern).parse()
            self.assertEqual(result, {"company": {"employees": [{"name": "Ivan"}, {"name": "Judy"}]}})

if __name__ == "__main__":
    unittest.main()