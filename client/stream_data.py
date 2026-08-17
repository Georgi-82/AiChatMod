import asyncio
import json
import websockets


mock_logs = ["error log incorrect","error out of memory exception","error database connection pool exhausted","error system test trigger log"]

async def send_log_stream():
    async with websockets.connect("ws://localhost:8000/ws") as websocket:
        for i in mock_logs:
            print(f"i am about to send{i}")
            await websocket.send(i)
            await asyncio.sleep(0.1)

        print("📥 Awaiting batch calculation matrix from local AI engine...")
        for _ in range(len(mock_logs)):
            response = await websocket.recv()
            print(f"📊 AI System Analytics Response: {response}")


if __name__ == "__main__":
    # Boots up the local asyncio event engine to execute your function
    asyncio.run(send_log_stream())