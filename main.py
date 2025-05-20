from fastapi import FastAPI, WebSocket
from api.routes import router as api_router
from websocket.websocket_manager import websocket_endpoint

app = FastAPI()
app.include_router(api_router)


@app.websocket("/ws/{player_name}")
async def websocket_handler(websocket: WebSocket, player_name: str):
    await websocket_endpoint(websocket, player_name)
