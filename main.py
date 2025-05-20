from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from api.routes import router as api_router
from websocket.websocket_manager import websocket_endpoint
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(api_router)

# Configure CORS to test using a browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development purposes, might need to be adjusted for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/test")
def get_test_ui():
    return FileResponse("static/test.html")


@app.websocket("/ws/{player_name}")
async def websocket_handler(websocket: WebSocket, player_name: str):
    await websocket_endpoint(websocket, player_name)
