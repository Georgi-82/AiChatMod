from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
from model  import AIModelAgent

app  = FastAPI()
queue = asyncio.Queue()



@app.on_event("startup")
async def startup_event():
    asyncio.create_task(dynamic_batch_worker)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await websocket.accept()
        while True:
            data = await websocket.receive_text()
            dict = {"text":data,"ws":websocket}
            queue.put_nowait(dict)

    except WebSocketDisconnect:
        print("Network is disconnected")

AiModel = AIModelAgent()
@app.websocket("/ws")

async def dynamic_batch_worker():

    while True:
        first_message = await queue.get()
        messages = [first_message]
        while len(messages) <= 4:
            try:
                message = queue.get_nowait()
                messages.append(message)
            except asyncio.QueueEmpty :
                break

            texts = [messages["text"] for _ in messages ]

        scores = await asyncio.to_thread(AiModel.classify_log,texts)

        for index,message in enumerate(messages):
            client = message["ws"]
            ai_score  = scores[index]
            try :
                await client.send_text(ai_score)

            except:
                print("connection failed")

        for _ in range(len(messages)):
            queue.task_done()

            

            


        

        
