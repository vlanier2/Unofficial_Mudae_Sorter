import tkinter as tk
import nameshower as ns


class CategoryBrowser(tk.Frame):
    def __init__(self, master, catdict, **kw):
        tk.Frame.__init__(self, master, **kw)
        self.pack_propagate(0)
        self.listeners = []

        self.catdict = catdict
        self.categories = list(self.catdict.keys())
        self.namelist = list(self.catdict.values())
        self.category_bound = [0, len(self.categories)-1]
        self.current_category = 0

        self.leftbutton = tk.Button(self, text='<-', command=self._shift_left)
        self.leftbutton.pack(side=tk.LEFT)

        self.rightbutton = tk.Button(self, text='->', command=self._shift_right)
        self.rightbutton.pack(side=tk.RIGHT)

        self.catname = ns.NameShower(self)
        self.catname.pack()

        self.textbox = tk.Text(self, width=50, height=35)
        self.textbox.pack()

        self.newcat_name = tk.Text(self, width=50, height=1)
        self.newcat_name.pack(pady=(100,0))

        self.newcat_button = tk.Button(self, text='Make New Category', command=self._new_category)
        self.newcat_button.pack()

        self.newcat_button = tk.Button(self, text='Save Categories', command=self._update_category)
        self.newcat_button.pack()

        try:
            self._show_category(0)
        except IndexError:
            pass

    def add_listener(self, other):
        self.listeners.append(other)

    def _new_category(self):
        name = self.newcat_name.get('1.0', 'end - 1c')
        if name.strip() == '':
            return
        self.newcat_name.delete('1.0', 'end - 1c')
        self.catdict[name] = []
        self._update_dict()

        for listener in self.listeners:
            listener.notify(name)

        if self.category_bound == [0,0]:
            self.catname.notify(name)

    def get_dictionary(self):
        return self.catdict

    def _update_category(self):
        category = self.categories[self.current_category]
        new = self.textbox.get('1.0', 'end - 1c').strip().split('\n')
        self.catdict[category] = new
        self._update_dict()

    def _update_dict(self):
        self.categories = list(self.catdict.keys())
        self.namelist = list(self.catdict.values())
        self.category_bound = [0, len(self.categories)-1]

    def _show_category(self, index):
        self.textbox.delete('1.0', 'end - 1c')
        for name in self.namelist[index]:
            self.textbox.insert('end', name + '\n')
        self.catname.notify(self.categories[index])

    def _shift_right(self):
        if self.current_category != self.category_bound[1]:
            self._update_category()
            self.current_category += 1
            self._show_category(self.current_category)

    def _shift_left(self):
        if self.current_category != self.category_bound[0]:
            self._update_category()
            self.current_category -= 1
            self._show_category(self.current_category)

if __name__ == '__main__':

    root = tk.Tk()
    catdict = {}#{'cat1': ['a','b','c'], 'cat2' : ['d','e','f'], 'cat3':['ee','eeee','eeee']}
    catbrow = CategoryBrowser(root, catdict, width=700, height=900, bg='light blue')
    catbrow.pack()
    root.mainloop()