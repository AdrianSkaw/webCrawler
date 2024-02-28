from abc import ABC, abstractmethod


class ParsingStrategy(ABC):
    @abstractmethod
    def parse(self, content: str) -> dict:
        pass


class TextParsingStrategy(ParsingStrategy):
    """A strategy for parsing text."""

    def parse(self, content: str) -> dict:
        # Implement text parsing logic
        pass


class AttributeParsingStrategy(ParsingStrategy):
    """A strategy for parsing attributes."""

    def parse(self, content: str) -> dict:
        # Implement attribute parsing logic
        pass
