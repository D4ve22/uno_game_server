from game.card import Card, Color


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
        if card.value == "skip":
            game.next_turn()
        elif card.value == "+2":
            next_player = game.players[(game.current_player_index + 1) % len(game.players)]
            for _ in range(2):
                next_player.draw_card(game.deck.draw())
        elif card.value == "+4":
            next_player = game.players[(game.current_player_index + 1) % len(game.players)]
            for _ in range(4):
                next_player.draw_card(game.deck.draw())
