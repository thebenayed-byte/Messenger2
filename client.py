import asyncio
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import simpledialog
import websockets

SERVER = "wss://messenger2-dxp7.onrender.com/chat"

class ChatClient:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Ben Chat")
        self.root.geometry("500x600")

        self.name = simpledialog.askstring("Pseudo", "Votre pseudo :")

        if not self.name:
            self.name = "Anonyme"

        self.chat = ScrolledText(self.root, state="disabled")
        self.chat.pack(fill="both", expand=True, padx=5, pady=5)

        self.entry = tk.Entry(self.root, font=("Arial",12))
        self.entry.pack(fill="x", padx=5, pady=5)
        self.entry.bind("<Return>", self.send_message)

        self.button = tk.Button(
            self.root,
            text="Envoyer",
            command=self.send_message
        )
        self.button.pack(fill="x", padx=5)

        self.loop = asyncio.new_event_loop()
        self.ws = None

        threading.Thread(target=self.start_loop, daemon=True).start()

        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.root.mainloop()

    def start_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.connect())

    async def connect(self):

        try:
            self.ws = await websockets.connect(SERVER)

            self.add_message("Connecté au serveur.")

            while True:

                msg = await self.ws.recv()

                self.root.after(
                    0,
                    lambda m=msg: self.add_message(m)
                )

        except Exception as e:

            self.root.after(
                0,
                lambda: self.add_message("Erreur : "+str(e))
            )

    def add_message(self,message):

        self.chat.configure(state="normal")
        self.chat.insert(tk.END,message+"\n")
        self.chat.see(tk.END)
        self.chat.configure(state="disabled")

    def send_message(self,event=None):

        if self.ws is None:
            return

        text=self.entry.get().strip()

        if text=="":

            return

        message=f"{self.name} : {text}"

        asyncio.run_coroutine_threadsafe(
            self.ws.send(message),
            self.loop
        )

        self.entry.delete(0,tk.END)

    def close(self):

        if self.ws:

            asyncio.run_coroutine_threadsafe(
                self.ws.close(),
                self.loop
            )

        self.root.destroy()


ChatClient()
