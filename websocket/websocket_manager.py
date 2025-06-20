from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict
import api.routes
from game.game import Game, Player
import uuid

connections: Dict[str, WebSocket] = {}


async def websocket_endpoint(ws: WebSocket, player_name: str):
    await ws.accept()
    player_id = str(uuid.uuid4())
    player = Player(id=player_id, name=player_name)
    connections[player_id] = ws
    if not api.routes.game.name_available(player_name):
        await send_to_player(player_id, "name_already_in_use", {})
        await ws.close()
        del connections[player_id]
        return
    if api.routes.game.add_player(player):
        await send_to_player(player_id, "join_success", {"id": player_id})
        await broadcast("player_joined", {"player_name": player.name})
        if api.routes.game.start_game():
            await broadcast("game_started", {})
            await send_to_player(api.routes.game.get_current_player().id, "your_turn", {"action": None})
    else:
        await send_to_player(player_id, "join_failed_game_full", {})
        await ws.close()
        del connections[player_id]
        return
    try:
        while True:
            data = await ws.receive_json()
            # Handle message
    except WebSocketDisconnect:
        del connections[player_id]
        leaving_player = api.routes.game.get_player(player_id)
        api.routes.game.remove_player(player_id)
        if api.routes.game.started and len(api.routes.game.players) == 1:
            winner = api.routes.game.players[0]
            await broadcast("game_won", {"winner": winner.name})
            api.routes.game = Game()    # reset
            for player in connections:
                await connections[player].close()
        else:
            await broadcast("player_left", {"player_name": leaving_player.name})


async def send_to_player(player_id: str, event: str, data):
    if player_id in connections:
        await connections[player_id].send_json({"event": event, "data": data})


async def broadcast(event: str, data):
    for ws in connections.values():
        await ws.send_json({"event": event, "data": data})


async def close_all_connections():
    for player_id, ws in list(connections.items()):
        try:
            await ws.close()
        except:
            pass
        del connections[player_id]
