from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
from server.model import AiModel

app = FastAPI()
queue = asyncio.Queue()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(dynamic_batch_worker())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await websocket.accept()
        while True:
            data = await websocket.receive_text()
            log_packet = {"text": data, "ws": websocket}
            queue.put_nowait(log_packet)
    except WebSocketDisconnect:
        print("🔌 Network is disconnected safely.")

async def dynamic_batch_worker():
    while True:
        first_message = await queue.get()
        messages = [first_message]
        
        while len(messages) < 4:
            try:
                message = queue.get_nowait()
                messages.append(message)
            except asyncio.QueueEmpty:
                break

        # 🟢 Correctly extract the raw text elements out of the memory list
        texts = [item["text"] for item in messages]

        scores = await asyncio.to_thread(AiModel.classify_log, texts)

        for index, message in enumerate(messages):
            client = message["ws"]
            ai_score = scores[index]
            try:
                # 🟢 Cast to a string so it travels smoothly across the network wire
                await client.send_text(str(ai_score))
            except Exception:
                print("⚠️ Transmission failed. Socket dead.")

        for _ in range(len(messages)):
            queue.task_done()


            

            


        

        
