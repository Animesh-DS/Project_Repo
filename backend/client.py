import asyncio
import websockets

async def test_connection():
    uri = "ws://127.0.0.1:8000/ws/pipeline"
    print(f"Attempting to connect to {uri}...")
    try:
        async with websockets.connect(uri) as websocket:
            print("🟢 SUCCESS! Python bypassed the browser and connected!")
            await websocket.send("Hello from Python!")
    except Exception as e:
        print(f"🔴 FAILED: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())