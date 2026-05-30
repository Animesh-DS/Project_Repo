from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws/test")
async def test_websocket(websocket: WebSocket):
    await websocket.accept()
    print("⭐⭐⭐ THE WEBSOCKET IS ALIVE! ⭐⭐⭐")
    while True:
        data = await websocket.receive_text()