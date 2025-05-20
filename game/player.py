from typing import List
from game.card import Card


class Player:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
        self.hand: List[Card] = []
        self.websocket = None

    def draw_card(self, card: Card):
        self.hand.append(card)

    def has_card(self, card: Card):
        return card in self.hand

    def play_card(self, card: Card):
        if card in self.hand:
            self.hand.remove(card)
            return True
        return False

    def has_uno(self):
        return len(self.hand) == 1
