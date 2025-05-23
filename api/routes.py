from fastapi import APIRouter
from game.game import Game
from websocket.websocket_manager import broadcast, send_to_player, close_all_connections
from game.card import Card, Color, Value
from game.player import Player

router = APIRouter()
game = Game()


@router.get("/hand/{player_id}")
def get_hand(player_id: str):
    if not game.started:
        return {"error": "no_current_game"}
    player = game.get_player(player_id)
    if player:
        return {"hand": [vars(card) for card in player.hand]}
    return {"error": "player_not_found"}


@router.get("/play/{player_id}/{color}/{value}")
async def play_card(player_id: str, color: str, value: str):
    global game
    if not game.started:
        return {"error": "no_current_game"}
    if player_id == game.get_current_player().id:
        try:
            enum_color = Color(color.lower())
            enum_value = Value(value.lower())
        except:
            return {"error": "card_not_valid"}
        card = Card(color=enum_color, value=enum_value)
        current_player = game.get_current_player()
        success = game.play_card(player_id, card)
        if success:
            await broadcast("card_played", {
                "player": current_player.name,
                "card": {
                    "color": card.color.value,
                    "value": card.value.value
                }
            })
            if len(current_player.hand) == 0:
                await broadcast("game_won", {"winner": current_player.name})
                await close_all_connections()
                game = Game()  # reset
            else:
                if current_player.has_uno():
                    await broadcast("uno_called", {"player": current_player.name})
                next_player = game.get_current_player()
                discarded_card = game.discard_pile
                if discarded_card.is_action_card():
                    await send_next_turn_information(next_player, discarded_card.value)
                else:
                    await send_next_turn_information(next_player, None)
            return {"status": "card_played"}
        return {"error": "invalid_move"}
    return {"error": "not_your_turn"}


@router.get("/draw/{player_id}")
async def draw_card(player_id):
    if not game.started:
        return {"error": "no_current_game"}
    if player_id == game.get_current_player().id:
        current_player = game.get_current_player()
        card = game.draw_card(player_id)
        if card:
            await broadcast("card_drawn", {
                "player": current_player.name
            })
            return {"card": vars(card)}
        return {"error": "no_card_drawn"}
    return {"error": "not_your_turn"}


@router.get("/state")
def get_state():
    return game.get_game_state()


async def send_next_turn_information(next_player: Player, action):
    await send_to_player(next_player.id, "your_turn", {"action": None if action is None else action.value})

