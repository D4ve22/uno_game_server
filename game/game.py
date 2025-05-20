from typing import List, Optional
from game.player import Player
from game.deck import Deck
from game.card import Card
from game.uno_rules import UnoRules


class Game:
    def __init__(self):
        self.players: List[Player] = []
        self.deck = Deck()
        self.discard_pile: Card = None
        self.current_player_index: int = 0
        self.started: bool = False

    def add_player(self, player: Player):
        if not self.started and len(self.players) < 2:
            self.players.append(player)
            return True
        return False

    def remove_player(self, player_id: str):
        self.players = [p for p in self.players if p.id != player_id]

    def get_player(self, player_id: str) -> Optional[Player]:
        for player in self.players:
            if player_id == player.id:
                return player
        return None

    def start_game(self):
        if len(self.players) == 2:
            self.deck.shuffle()
            for player in self.players:
                for _ in range(7):
                    player.hand.append(self.deck.draw())
            self.discard_pile = self.deck.draw()
            self.started = True
            return True
        return False

    def get_current_player(self) -> Player:
        if len(self.players) > 0:
            return self.players[self.current_player_index]
        return None

    def play_card(self, player_id: str, card: Card):
        player = self.get_player(player_id)
        if player and UnoRules.is_valid_move(self.discard_pile, card) and player.has_card(card):
            player.play_card(card)
            self.deck.put(self.discard_pile)
            self.discard_pile = card
            UnoRules.apply_card_effect(card, self)
            self.next_turn()
            return True
        return False

    def draw_card(self, player_id: str):
        player = self.get_player(player_id)
        if player:
            card = self.deck.draw()
            if card:
                player.hand.append(card)
            return card
        return None

    def next_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def get_game_state(self):
        current_player = None if self.get_current_player() is None else self.get_current_player().name
        return {
            "started": self.started,
            "players": [p.name for p in self.players],
            "current_player": current_player,
            "top_discard": vars(self.discard_pile) if self.discard_pile else None
        }

    def name_available(self, name):
        for player in self.players:
            if name == player.name:
                return False
        return True
