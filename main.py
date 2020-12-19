'''
main.py - main driver for the sorting app.
    Running main opens control panel.
'''
import tkinter as tk
import linkeditor
import categoryeditor as ce
import sorteditor as se

class ControlPanel(tk.Tk):
    def __init__(self, **kw):
        tk.Tk.__init__(self, **kw)
        self.open_windows = {'link': None,
                            'category': None,
                            'sort': None}
        self.recently_added = []

    def notify(self, code):
        try:
            if code == 'new entries':
                self.open_windows['category'].get_recenty_added()

        except AttributeError:
            pass

controlpanel = ControlPanel()
controlpanel.title('Image Sorter')
controlpanel.geometry('600x400')

frame = tk.Frame(controlpanel, width=600, height=400, bg='light blue')
frame.pack(side=tk.LEFT)
frame.pack_propagate(0)

button1 = tk.Button(frame, text='Edit Image Links',
                    command=lambda: linkeditor.openwindow(controlpanel))
button1.pack(anchor=tk.NW)

button2 = tk.Button(frame, text='Redo Categories',
                    command=lambda: ce.openwindow(controlpanel))
button2.pack(anchor=tk.NW)

button3 = tk.Button(frame, text='Sort Categories',
                    command=lambda: se.openwindow(controlpanel))
button3.pack(anchor=tk.NW)

controlpanel.mainloop()