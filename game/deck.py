from game.card import Card, Color, Value
import random
from typing import List


class Deck:
    def __init__(self):
        self.cards = self.generate_deck()
        self.shuffle()

    @staticmethod
    def generate_deck():
        cards: List[Card] = []
        for i in range(4):
            cards.append(Card(Color.BLACK, Value.PLUS_4))

        for color in list(Color)[:-1]:
            cards.append(Card(color, Value.ZERO))

        for i in range(0, 2):
            for color in list(Color)[:-1]:
                for value in list(Value)[1:-1]:
                    cards.append(Card(color, value))
        return cards

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        self.shuffle()
        return self.cards.pop() if self.cards else None

    def put(self, card: Card):
        self.cards.append(card)
        self.shuffle()

    def reset(self):
        self.cards = self.generate_deck()
        self.shuffle()
