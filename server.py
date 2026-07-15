from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

app = FastAPI()
@app.get("/")
def home():
    return {
        "status": "BenChat est en ligne",
        "websocket": "/chat"
    }
clients = []

@app.websocket("/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    try:
        while True:
            message = await websocket.receive_text()

            for client in clients:
                await client.send_text(message)

    except WebSocketDisconnect:
        clients.remove(websocket)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
