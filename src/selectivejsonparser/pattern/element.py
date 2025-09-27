from typing import Set

class Element:
    def __init__(self) -> None:
        raise NotImplementedError("Element is an abstract base class and cannot be instantiated directly.")
    
class Key(Element):
    def __init__(self) -> None:
        self.entries: Set[str] = set()

    def add(self, entry: str) -> None:
        self.entries.add(entry)

    def __contains__(self, entry: str) -> bool:
        return entry in self.entries
    
class Index(Element):
    def __init__(self) -> None:
        pass

class Anything(Element):
    def __init__(self) -> None:
        pass