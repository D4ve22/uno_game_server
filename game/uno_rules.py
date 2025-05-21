import api.routes
from game.card import Card, Color, Value


class UnoRules:
    @staticmethod
    def is_valid_move(current_card: Card, new_card: Card):
        return (
            new_card.color == current_card.color or
            new_card.value == current_card.value or
            new_card.color == Color.BLACK or
            current_card.color == Color.BLACK
        )

    @staticmethod
    def apply_card_effect(card: Card, game):
        print(card.value)
        if card.value == Value.SKIP:
            print("Vor next turn:", game.get_current_player())
            game.next_turn()
            print("Nach next turn:", game.get_current_player())
            api.routes.send_next_turn_information(game.get_current_player(), game.discard_pile.value)
        elif card.value == Value.PLUS_2:
            next_player = game.players[(game.current_player_index + 1) % len(game.players)]
            for _ in range(2):
                next_player.draw_card(game.deck.draw())
        elif card.value == Value.PLUS_4:
            next_player = game.players[(game.current_player_index + 1) % len(game.players)]
            for _ in range(4):
                next_player.draw_card(game.deck.draw())
