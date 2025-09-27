from typing import Iterator, List, Optional

from selectivejsonparser.pattern.element import Element, Key, Index, Anything

class PatternParser:
    def __init__(self, pattern: str) -> None:
        self.elements: List[Element] = []
        self.pattern: str = pattern
        self.position: int = 0

    def parse(self) -> Iterator[Element]:
        while True:
            element: Optional[Element] = self._parse_key()
            if element is None:
                element = self._parse_index()
            if element is None:
                break
            yield element
            if self._dot():
                self._advance()
            elif self._opening_bracket():
                continue
        yield Anything()
        if not self._end():
            raise ValueError(f"Unexpected character at position {self.position}: '{self._char()}'")
        
    
    def _parse_key(self) -> Optional[Key]:
        key = Key()
        if self._star():
            key.add("*")
            self._advance()
            return key
        while self._alphanumeric():
            start = self.position
            while self._alphanumeric():
                self._advance()
            key.add(self.pattern[start:self.position])
            if self._or():
                self._advance()
            else:
                break
        if not key.entries:
            return None
        return key
    
    def _parse_index(self) -> Optional[Index]:
        if not self._opening_bracket():
            return None
        self._advance()
        if not self._closing_bracket():
            raise ValueError("Expected closing bracket for index")
        self._advance()
        return Index()
    
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