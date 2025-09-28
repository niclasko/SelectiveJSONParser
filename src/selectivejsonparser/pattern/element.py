from typing import Dict, List, Optional, Self

class Element:
    def __init__(self) -> None:
        self.parent: Optional[Element] = None

    def set_parent(self, parent: Self) -> None:
        self.parent = parent

class Dictionary(Element):
    def __init__(self) -> None:
        super().__init__()
        self.children: Dict[str, Element] = {}

    def __setitem__(self, key: str, child: Element) -> None:
        self.children[key] = child
        child.set_parent(self)

    def __getitem__(self, key: str) -> Optional[Element]:
        if key not in self.children:
            return None
        return self.children[key]

    def __contains__(self, key: str) -> bool:
        return key in self.children

class Array(Element):
    def __init__(self) -> None:
        super().__init__()
        self.children: List[Element] = []

    def append(self, element: Element) -> None:
        self.children.append(element)
        element.set_parent(self)

    def __getitem__(self, index: int) -> Optional[Element]:
        if index < len(self.children):
            return self.children[index]
        return None

class Value(Element):
    def __init__(self) -> None:
        super().__init__()

    def __getitem__(self, key: str) -> Optional[Element]:
        return None