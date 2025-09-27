from typing import Union, Optional, List

from selectivejsonparser.pattern import PatternParser
from selectivejsonparser.pattern.element import Element, Key, Index, Anything

class Pattern:
    def __init__(self, pattern: Optional[str]) -> None:
        self.elements: Optional[List[Element]] = list(PatternParser(pattern).parse()) if pattern else None
        self.position = 0
    
    def key(self, value: str) -> bool:
        element: Optional[Element] = self.element()
        self._next()
        return isinstance(element, Key) and value in element
    
    def index(self) -> bool:
        element: Optional[Element] = self.element()
        self._next()
        return isinstance(element, Index)
    
    def anything(self) -> bool:
        element: Optional[Element] = self.element()
        self._next()
        return isinstance(element, Anything)
    
    def _next(self) -> None:
        self.position += 1

    def previous(self) -> None:
        self.position -= 1
        
    def element(self) -> Optional[Element]:
        if self.position >= len(self.elements):
            return None
        return self.elements[self.position]
        