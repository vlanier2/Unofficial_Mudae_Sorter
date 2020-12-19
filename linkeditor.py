'''
linkeditor.py 
CONTENTS:
    link editor window class 
    open function for link editor
'''
import tkinter as tk
from tkinter import messagebox
from utilities import get_recently_appended

WINDOW_GEOMETRY = '800x800'

def openwindow(controller):
    global linkeditor
    try:
        linkeditor.focus()
    except NameError:
        linkeditor = Window(controller)
        linkeditor.title('LinkFile Editor')
        linkeditor.geometry(WINDOW_GEOMETRY)
        linkeditor.protocol('WM_DELETE_WINDOW', linkeditor.on_close)
        controller.open_windows['link'] = linkeditor


class Window(tk.Toplevel):
    def __init__(self, controller, **kw):
        tk.Toplevel.__init__(self, **kw)
        self.controller = controller
        
        self.frame = tk.Frame(self, width=800, height=800, bg='green')
        self.frame.pack()
        self.frame.pack_propagate(0)

        self.textin = tk.Text(self.frame, width=100)
        self.textin.pack(pady=100)
        
        self.new_linkfile_button = tk.Button(self.frame, text='Clear LinkFile', 
                                                command=self._new_linkfile)
        self.new_linkfile_button.pack()

        self.append_linkfile_button = tk.Button(self.frame, text='Add to LinkFile',
                                                    command=self._append_linkfile)
        self.append_linkfile_button.pack()

    def _new_linkfile(self):
        if messagebox.askokcancel("Yes", "This will clear the LinkFile, are you sure?"):
            open('linkfile.txt', 'w').close()
            self.controller.recetly_added = []

    def _append_linkfile(self):
        text = self.textin.get('1.0', 'end-1c')
        with open('linkfile.txt', 'a') as linkfile:
            linkfile.write(text)
        self.controller.recently_added += get_recently_appended(text)
        self.controller.notify('new entries')
        
    def on_close(self):
        self.controller.open_windows['link'] = None
        self.destroy()
        del globals()['linkeditor']
