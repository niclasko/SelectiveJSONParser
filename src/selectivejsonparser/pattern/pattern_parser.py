from typing import List, Optional, Set

from selectivejsonparser.pattern.element import Element, Dictionary, Array, Value

class PatternParser:
    """Parses a pattern string into its component elements.

    Args:
    - pattern: The pattern string to parse.

    Examples of patterns:
        "key1.key2[key3]" -> {"key1": {"key2": [{"key3": ...}]}}
        "key1|key2.key3" -> {"key1" or "key2": {"key3": ...}}
        "[key1]" -> [{"key1": ...}, {"key1": ...}, ...]
    """
    def __init__(self, pattern: str) -> None:
        self.elements: List[Element] = []
        self.pattern: str = pattern
        self.position: int = 0

    def parse(self) -> Optional[Element]:
        element: Optional[Element] = self._parse_dictionary()
        if element is None:
            element = self._parse_array()
        return element

    def _parse_dictionary(self) -> Optional[Dictionary]:
        if self._dot():
            self._advance()
        parentheses: bool = self._opening_parenthesis()
        if parentheses:
            self._advance()
        if not self._alphanumeric():
            return None
        keys: Set[str] = set()
        while True:
            start: int = self.position
            while self._alphanumeric():
                self._advance()
            keys.add(self.pattern[start:self.position])
            if not self._or():
                break
            self._advance()
        if parentheses and self._closing_parenthesis():
            self._advance()
        elif parentheses and not self._closing_parenthesis():
            raise ValueError("Expected closing parenthesis")
        element: Dictionary = Dictionary()
        child: Optional[Element] = self.parse()
        for key in keys:
            element[key] = child if child else Value()
        return element

    def _parse_array(self) -> Optional[Array]:
        if not self._opening_bracket():
            return None
        self._advance()
        element: Optional[Element] = self.parse()
        if not self._closing_bracket():
            raise ValueError("Expected closing bracket")
        self._advance()
        array: Array = Array()
        array.append(element if element else Value())
        return array

    def _char(self) -> Optional[str]:
        if self.position < len(self.pattern):
            return self.pattern[self.position]
        return None
    
    def _advance(self) -> None:
        self.position += 1

    def _opening_bracket(self) -> bool:
        return self._char() == '['
    
    def _closing_bracket(self) -> bool:
        return self._char() == ']'

    def _opening_parenthesis(self) -> bool:
        return self._char() == '('
    
    def _closing_parenthesis(self) -> bool:
        return self._char() == ')'
    
    def _dot(self) -> bool:
        return self._char() == '.'
    
    def _star(self) -> bool:
        return self._char() == '*'
    
    def _alphanumeric(self) -> bool:
        char = self._char()
        return char is not None and (char.isalnum() or char == '_')
    
    def _or(self) -> bool:
        return self._char() == '|'

    def _end(self) -> bool:
        return self.position >= len(self.pattern)