import tkinter as tk

class NameShower(tk.Label):
    def __init__(self, master, **kw):
        tk.Label.__init__(self, master, **kw)

    def notify(self, text):
        self.configure(text=text)