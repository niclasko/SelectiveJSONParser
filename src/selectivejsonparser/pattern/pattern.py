from typing import Optional, Union, List

from selectivejsonparser.pattern import PatternParser
from selectivejsonparser.pattern.element import Element
class Pattern:
    def __init__(self, pattern: Optional[str]) -> None:
        self.element: Optional[Element] = PatternParser(pattern).parse() if pattern else None
        self.stack: List[Optional[Element]] = []

    def match(self, value: Optional[Union[str, int]] = None) -> None:
        self.stack.append(self.element)
        if self.element is None:
            return
        self.element = self.element[value]

    def backtrack(self) -> None:
        if not self.stack:
            return
        self.element = self.stack.pop()

    def is_selected(self) -> bool:
        if self.element is None:
            return True
        return self.element.is_selected()