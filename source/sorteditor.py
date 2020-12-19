import tkinter as tk
from tkinter import ttk
import pickle
from PIL import ImageTk, Image
import sortinggrid as sg
from utilities import parse_linkfile
import nameshower as ns
from tkinter import messagebox

WINDOW_GEOMETRY = '1600x900'

def openwindow(controller):
    global sorteditor
    try:
        sorteditor.focus()
    except NameError:
        sorteditor = Window(controller)
        sorteditor.title('Sort Editor')
        sorteditor.geometry(WINDOW_GEOMETRY)
        sorteditor.protocol('WM_DELETE_WINDOW', sorteditor.on_close)
        controller.open_windows['sort'] = sorteditor

class Window(tk.Toplevel):
    def __init__(self, controller, **kw):
        tk.Toplevel.__init__(self, **kw)
        self.controller = controller

        with open('category_dict', 'rb') as src:    
            self.cat_dict = pickle.load(src)
            print(self.cat_dict)

        with open('linkfile.txt') as lf:
            all_names, links = parse_linkfile(lf)
            self.link_dict = dict(zip(all_names, links))

        tab_parent = ttk.Notebook(self)

        self.grids = []
        for category in list(self.cat_dict.keys()):
            tab = ttk.Frame(tab_parent)
            grid = sg.SortingGrid(tab, (63, 98), width=1200, height=900,
                                    link_dict = self.link_dict, names=self.cat_dict[category])
            grid.pack(side=tk.LEFT)
            self.grids.append(grid)

            # right hand frame
            frame = tk.Frame(tab, width=1200, height=900, bg='light blue')
            frame.pack(side=tk.LEFT)
            frame.pack_propagate(0)

            namedisplay = ns.NameShower(frame, text="name", font='none 12')
            namedisplay.pack(side=tk.TOP)

            grid.listeners.append(namedisplay)
            tab_parent.add(tab, text=category)

        button = tk.Button(frame, text='Get Commands', command=self._getstrings)
        button.pack(side=tk.TOP)

        self.textout = tk.Text(frame, width=20, height=50)
        self.textout.pack(side=tk.TOP)
            
        tab_parent.pack(expand=1, fill='both')

    def _getstrings(self):
        sorted_names = []
        for grid in self.grids:
            sorted_names += grid.getSortedNames()
        string = '$sortmarry '+ '$'.join(sorted_names)
        self.textout.delete('1.0', 'end')
        self.textout.insert('1.0', string)
        

    def on_close(self):
        self.controller.open_windows['sort'] = None
        self.destroy()
        del globals()['sorteditor']




# if __name__ == '__main__':
#     root = tk.Tk()
#     root.geometry = "800x800"
#     tab_parent = ttk.Notebook(root)
#     tab1 = ttk.Frame(tab_parent)
#     tab2 = ttk.Frame(tab_parent)
#     tab_parent.add(tab1, text="All Records")
#     tab_parent.add(tab2, text="Add New Record")
#     tab_parent.pack(expand=1, fill='both')
#     root.mainloop()