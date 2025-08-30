import asyncio, websockets, json

async def test_ws():
    uri = "ws://127.0.0.1:8000/ws/meetings/testroom/"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({"message": "Hello from Python"}))
        response = await websocket.recv()
        print("Response:", response)

asyncio.run(test_ws())
