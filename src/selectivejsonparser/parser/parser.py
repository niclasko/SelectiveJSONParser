from typing import Optional, Any, Dict, List, Iterator, Tuple, Union, TypeVar

from selectivejsonparser.pattern import Pattern

null = TypeVar("null")
unexpected = TypeVar("unexpected")
json = TypeVar("json", Dict[str, Any], List[Any], None)
atom = TypeVar("atom", str, int, float, bool, null, unexpected)

class Parser:
    """A simple JSON parser that can parse JSON objects and arrays from a string.

    Attributes:
        text (str): The JSON string to parse.
        position (int): The current position in the string.
        pattern (str): The path pattern to extract specific values.

        Example patterns:
            - "key1" to extract the value of "key1" from the root object.
            - "key1.key2" to extract the value of "key2" inside the object "key1".
            - "key1[].key2" to extract the value of "key2" inside the first object of the array "key1".
            - "[].key1" to extract the value of "key1" inside the first object of the root array.
            - "[].key1" to extract the values of "key1" from all objects in the root array.
            - "key1|key2" to extract the value of "key1" or "key2" (whichever exists first) from the root object.
            - "[].key1|key2.key3" to extract the value of "key3" from all objects in the root array, where each object has either "key1" or "key2".

    """
    def __init__(self, text: str, pattern: Optional[str] = None) -> None:
        self.text: str = text
        self.position: int = 0
        self.pattern: Optional[Pattern] = Pattern(pattern)

    def parse(self) -> json:
        self._skip_whitespace()
        result: json = self._parse_dict()
        if result is None:
            result = self._parse_list()
        self._skip_whitespace()
        if self.position != len(self.text):
            raise ValueError("Unexpected data after JSON value")
        if result is None:
            raise ValueError("No JSON object or array found")
        return result
    
    def _parse_dict(self) -> Optional[Dict[str, Any]]:
        if not self._opening_curly_brace():
            return None
        self._advance()
        self._skip_whitespace()
        parsed: Dict[str, Any] = dict(self._parse_dict_entries())
        self._skip_whitespace()
        if not self._closing_curly_brace():
            raise ValueError("Expected closing curly brace")
        self._advance()
        return parsed
    
    def _parse_dict_entries(self) -> Iterator[Tuple[str, Any]]:
        more: bool = False
        while True:
            self._skip_whitespace()
            key: Optional[str] = self._parse_string()
            if key is None and not more:
                break
            elif key is None and more:
                raise ValueError("Expected string key")
            self._skip_whitespace()
            if not self._colon():
                raise ValueError("Expected colon after key")
            self._advance()
            self._skip_whitespace()
            match: bool = self.pattern.key(key)
            value: Optional[Any] = self._parse_value()
            self.pattern.previous()
            if value is None:
                raise ValueError("Expected value after colon")
            if match and value is not unexpected:
                yield (key, self._replace_with_none_if_is_null(value))
            self._skip_whitespace()
            if not self._comma():
                break
            more = True
            self._advance()
            self._skip_whitespace()
        
    def _parse_list(self) -> Optional[List[Any]]:
        if not self._opening_square_brace():
            return None
        self._advance()
        self._skip_whitespace()
        parsed: List[Any] = list(self._parse_list_items())
        self._skip_whitespace()
        if not self._closing_square_brace():
            raise ValueError("Expected closing square brace")
        self._advance()
        return parsed
    
    def _parse_list_items(self) -> Iterator[Any]:
        while True:
            self._skip_whitespace()
            match: bool = self.pattern.index()
            value: Optional[Any] = self._parse_value()
            self.pattern.previous()
            if value is None:
                break
            if match and value is not unexpected:
                yield self._replace_with_none_if_is_null(value)
            self._skip_whitespace()
            if not self._comma():
                break
            self._advance()
            self._skip_whitespace()

    def _parse_value(self) -> Optional[Union[atom, Dict[str, Any], List[Any]]]:
        value: Any = self._parse_dict()
        if value is None:
            value = self._parse_list()
        if value is None:
            value = self._parse_atom()
        if not self.pattern.anything():
            value = unexpected
        self.pattern.previous()
        return value
    
    def _parse_atom(self) -> Optional[atom]:
        value: Any = None
        value = self._parse_string()
        if value is None:
            value = self._parse_number()
        if value is None:
            value = self._parse_boolean()
        if value is None:
            value = self._parse_null()
        return value
    
    def _parse_string(self) -> Optional[str]:
        if not self._quote():
            return None
        self._advance()
        start = self.position
        while not self._quote():
            if self.position >= len(self.text):
                raise ValueError("Unterminated string")
            if self._char() == '\\' and self._next_char() == '"':
                self._advance()
            self._advance()
        string = self.text[start:self.position]
        self._advance()  # Skip closing quote
        return string
    
    def _parse_number(self) -> Optional[Union[int, float]]:
        start = self.position
        if self._char() in ('-', '+'):
            self._advance()
        while self._char() and self._char().isdigit():
            self._advance()
        if self._char() == '.':
            self._advance()
            while self._char() and self._char().isdigit():
                self._advance()
            if self._char() == 'e' or self._char() == 'E':
                self._advance()
                sub: int = self.position
                sign: bool = False
                if self._char() in ('-', '+'):
                    self._advance()
                    sign = True
                while self._char() is not None and self._char().isdigit():
                    self._advance()
                if sub == self.position or (sign and sub + 1 == self.position):
                    raise ValueError("Invalid number format")
            number: str = self.text[start:self.position]
            try:
                return float(number)
            except ValueError as exc:
                raise ValueError(f"Invalid number: {number}") from exc
        elif start != self.position:
            number: str = self.text[start:self.position]
            try:
                return int(number)
            except ValueError as exc:
                raise ValueError(f"Invalid number: {number}") from exc
        return None
    
    def _parse_boolean(self) -> Optional[bool]:
        if self.text.startswith("true", self.position):
            self.position += 4
            return True
        elif self.text.startswith("false", self.position):
            self.position += 5
            return False
        return None
    
    def _parse_null(self) -> Optional[null]:
        if self.text.startswith("null", self.position):
            self.position += 4
            return null
        return None
    
    def _replace_with_none_if_is_null(self, value: Any) -> Any:
        if value is null:
            return None
        return value

    def _skip_whitespace(self) -> None:
        while self._whitespace():
            self._advance()
    
    def _char(self) -> Optional[str]:
        if self.position >= len(self.text):
            return None
        return self.text[self.position]
    
    def _next_char(self) -> Optional[str]:
        if self.position + 1 >= len(self.text):
            return None
        return self.text[self.position + 1]
    
    def _previous_char(self) -> Optional[str]:
        if self.position - 1 < 0:
            return None
        return self.text[self.position - 1]

    def _opening_curly_brace(self) -> bool:
        return self._char() == '{'
    
    def _closing_curly_brace(self) -> bool:
        return self._char() == '}'
    
    def _opening_square_brace(self) -> bool:
        return self._char() == '['

    def _closing_square_brace(self) -> bool:
        return self._char() == ']'
    
    def _comma(self) -> bool:
        return self._char() == ','
    
    def _colon(self) -> bool:
        return self._char() == ':'
    
    def _quote(self) -> bool:
        return self._char() == '"'
    
    def _whitespace(self) -> bool:
        return self._char() in (' ', '\t', '\n', '\r')
    
    def _advance(self) -> None:
        self.position += 1