import asyncio
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import websockets

SERVER = "wss://ton-app.onrender.com/chat"

root = tk.Tk()
root.title("Ben Chat")

chat = ScrolledText(root)
chat.pack(fill="both", expand=True)

entry = tk.Entry(root)
entry.pack(fill="x")


async def receive():
    async with websockets.connect(SERVER) as ws:

        async def listen():
            while True:
                msg = await ws.recv()
                chat.insert(tk.END, msg + "\n")
                chat.see(tk.END)

        async def send_loop():
            while True:
                await asyncio.sleep(0.1)

        threading.Thread(target=lambda: asyncio.run(listen())).start()

        def send():
            text = entry.get()
            asyncio.run(ws.send(text))
            entry.delete(0, tk.END)

        tk.Button(root, text="Envoyer", command=send).pack()

        await send_loop()


asyncio.run(receive())