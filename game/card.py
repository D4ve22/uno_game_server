from enum import Enum


class Value(Enum):
    ZERO = "0"
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    SKIP = "skip"
    PLUS_2 = "+2"
    PLUS_4 = "+4"


class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    YELLOW = "yellow"
    BLACK = "black"


class Card:
    def __init__(self, color: Color, value: Value):
        self.color = color
        self.value = value

    def is_action_card(self):
        return self.value in {Value.PLUS_2, Value.PLUS_4, Value.SKIP}

    def __eq__(self, other):
        return isinstance(other, Card) and self.color == other.color and self.value == other.value

    def __repr__(self):
        return f"{self.color} {self.value}"
