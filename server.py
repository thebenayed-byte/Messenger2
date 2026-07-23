from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
import json

app = FastAPI()

@app.get("/")
def home():
    return {"status": "BenChat en ligne"}

# websocket -> pseudo
clients = {}

async def envoyer_utilisateurs():
    data = {
        "type": "users",
        "count": len(clients),
        "users": list(clients.values())
    }

    message = json.dumps(data)

    for ws in list(clients.keys()):
        try:
            await ws.send_text(message)
        except:
            pass

@app.websocket("/chat")
async def chat(websocket: WebSocket):

    await websocket.accept()

    try:
        # premier message = pseudo
        pseudo = await websocket.receive_text()

        clients[websocket] = pseudo

        print(f"{pseudo} connecté")

        await envoyer_utilisateurs()

        while True:

            texte = await websocket.receive_text()

            data = {
                "type": "message",
                "user": pseudo,
                "message": texte
            }

            message = json.dumps(data)

            for client in list(clients.keys()):
                await client.send_text(message)

    except WebSocketDisconnect:

        if websocket in clients:
            print(f"{clients[websocket]} déconnecté")
            del clients[websocket]

        await envoyer_utilisateurs()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
