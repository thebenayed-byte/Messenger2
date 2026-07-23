from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
import json

app = FastAPI()

@app.get("/")
def home():
    return {
        "status": "BenChat est en ligne",
        "websocket": "/chat"
    }

# Dictionnaire : websocket -> pseudo
clients = {}


async def envoyer_liste_utilisateurs():
    """Envoie la liste et le nombre de connectés à tout le monde"""

    data = {
        "type": "users",
        "count": len(clients),
        "users": list(clients.values())
    }

    message = json.dumps(data)

    for client in list(clients.keys()):
        try:
            await client.send_text(message)
        except:
            pass


@app.websocket("/chat")
async def chat(websocket: WebSocket):

    await websocket.accept()

    try:
        # Le premier message reçu est le pseudo
        pseudo = await websocket.receive_text()

        clients[websocket] = pseudo

        print(f"{pseudo} connecté")

        await envoyer_liste_utilisateurs()

        while True:
            message = await websocket.receive_text()

            data = {
                "type": "message",
                "user": pseudo,
                "message": message
            }

            texte = json.dumps(data)

            for client in list(clients.keys()):
                try:
                    await client.send_text(texte)
                except:
                    pass

    except WebSocketDisconnect:

        if websocket in clients:
            pseudo = clients[websocket]
            del clients[websocket]
            print(f"{pseudo} déconnecté")

        await envoyer_liste_utilisateurs()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
