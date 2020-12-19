'''
categoryeditor.py 
CONTENTS:
    category editor window class 
    open function for category editor
'''
import tkinter as tk
import pickle
from tkinter import messagebox
from utilities import parse_linkfile

WINDOW_GEOMETRY = '1600x900'

def openwindow(controller):
    global categoryeditor
    try:
        categoryeditor.focus()
    except NameError:
        categoryeditor = Window(controller)
        categoryeditor.title('Category Editor')
        categoryeditor.geometry(WINDOW_GEOMETRY)
        categoryeditor.protocol('WM_DELETE_WINDOW', categoryeditor.on_close)
        controller.open_windows['category'] = categoryeditor


class Window(tk.Toplevel):
    def __init__(self, controller, **kw):
        tk.Toplevel.__init__(self, **kw)
        self.controller = controller

        self.frame = tk.Frame(self, width=1600, height=900, bg='light blue')
        self.frame.pack()
        self.frame.pack_propagate(0)

        # Get Uncategorized Names
        self.textin = tk.Text(self.frame, width=50, height=50)
        self.textin.pack(side=tk.LEFT, padx=100)
        with open('linkfile.txt') as lf:
            names = parse_linkfile(lf)[0]
            for name in names:
                self.textin.insert('end', name + '\n')
        #self.get_recenty_added()

        # Dictionary to Hold Categories
        self.cat_dict = dict()
        self.cat_dict['uncategoried'] = []

### Ordering Box
        # Frame
        self.orderingframe = tk.Frame(self.frame, width=500, height=850, bg='red')
        self.orderingframe.pack(side=tk.LEFT)

        # Order Categories
        self.catorder = tk.Text(self.orderingframe, width=50, height=50)
        self.catorder.pack(side=tk.TOP)

        # Finalize Button
        self.finalized_button = tk.Button(self.orderingframe, text='Finalized Category Order', 
                                                            command=self._finalize_categories)
        self.finalized_button.pack(side=tk.BOTTOM)

### Category Box
        # Category Box Frame
        self.catmaker = tk.Frame(self.frame, width=500, height=850, bg='light green')
        self.catmaker.pack(side=tk.LEFT, padx=100)

        # Category Name Text Box
        self.cat_name = tk.Text(self.catmaker, width=20, height=2)
        self.cat_name.pack(side=tk.TOP)

        # Category Entry Text Box
        self.cat_entry = tk.Text(self.catmaker, width=50, height=50)
        self.cat_entry.pack()

        # Catergory Buttons
        self.finished_button = tk.Button(self.catmaker, text='Finish Category', command=self._make_category)
        self.finished_button.pack(side=tk.BOTTOM)

    def get_recenty_added(self):
        print(self.controller.recently_added)
        try:
            for name in self.controller.recently_added:
                self.textin.insert('1.0', name + '\n')
        except TypeError:
            pass

    def _make_category(self):
        title = self.cat_name.get('1.0', 'end-1c')
        names = self.cat_entry.get('1.0', 'end-1c').split('\n')

        self.cat_dict[title] = names
        self.cat_entry.delete('1.0', 'end') # clear the text 
        self.cat_name.delete('1.0', 'end')

        self.catorder.insert('end', title + '\n')

        print(self.cat_dict)

    def _finalize_categories(self):
        titles = self.catorder.get('1.0', 'end-1c').strip().split('\n')
        uncategoried = self.textin.get('1.0', 'end-1c').strip().split('\n')
        finaldict = {}

        for title in titles:
            finaldict[title] = self.cat_dict[title]

        if uncategoried != ['']:
            finaldict['uncategoried'] = uncategoried

        with open('category_dict', 'wb') as dest:
            pickle.dump(finaldict, dest)
        with open('category_dict', 'rb') as dest:
            finaldict = pickle.load(dest)
        print(finaldict)


    def on_close(self):
        self.controller.open_windows['category'] = None
        self.destroy()
        del globals()['categoryeditor']