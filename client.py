import asyncio
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import websockets

SERVER = "wss://https://messenger2-40wh.onrender.com/chat"

class ChatClient:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Ben Chat")

        self.chat = ScrolledText(self.root)
        self.chat.pack(fill="both", expand=True)

        self.entry = tk.Entry(self.root)
        self.entry.pack(fill="x")

        self.button = tk.Button(self.root, text="Envoyer", command=self.send)
        self.button.pack(fill="x")

        self.ws = None

        threading.Thread(target=self.start_loop, daemon=True).start()

        self.root.mainloop()

    def start_loop(self):
        asyncio.run(self.connect())

    async def connect(self):
        self.ws = await websockets.connect(SERVER)

        while True:
            msg = await self.ws.recv()

            self.chat.insert(tk.END, msg + "\n")
            self.chat.see(tk.END)

    def send(self):

        text = self.entry.get()

        if text == "":
            return

        asyncio.run_coroutine_threadsafe(
            self.ws.send(text),
            asyncio.get_event_loop()
        )

        self.entry.delete(0, tk.END)


ChatClient()
