import logging

from fastapi import FastAPI, WebSocket
from starlette.staticfiles import StaticFiles

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI()


connected = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected.add(websocket)
    try:
        # Forward messages
        while True:
            message = await websocket.receive_text()
            for client in connected:
                if client != websocket:
                    await client.send_text(message)
    finally:
        # Unregister.
        connected.remove(websocket)

app.mount("/", StaticFiles(directory="static"), name="static")
