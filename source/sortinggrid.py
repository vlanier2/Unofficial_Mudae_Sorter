import tkinter as tk
from PIL import ImageTk, Image
from utilities import parse_linkfile, get_url_dict, img_from_url
import nameshower

class SortingGrid(tk.Canvas):
    def __init__(self, master, tiledims, link_dict, names, **kw):
        self.tiledims = tiledims
        self.names = names
        self.link_dict = link_dict
        self.click_snaploc = None
        self.click_id = None
        self.listeners = []

        tk.Canvas.__init__(self, master, **kw)

        self.w = round(self.winfo_reqwidth()//tiledims[0]) * tiledims[0]
        self.h = round(self.winfo_reqheight()//tiledims[1]) * tiledims[1]

        ### draw grid
        for x in range(tiledims[0], self.w, tiledims[0]): # verticals
            self.create_line(x,0, x,self.h, tags='grid')

        for x in range(tiledims[1], self.h, tiledims[1]): # horizonals
            self.create_line(0,x, self.w,x, tags='grid')

        self.rank_map = self._get_rank_map()
        #print(self.rank_map)
        self.id_name_map = {}
        self.id_rank_map = {}

        global images
        if 'images' not in globals():
            images = []
        i, j = 0, 0
        for name in self.names:
            try:
                url = get_url_dict(self.link_dict, name)
                image = img_from_url(url, size=self.tiledims)
            except:
                image = Image.open('researchphoto.png').resize(self.tiledims)
                image = ImageTk.PhotoImage(image=image)
            
            x, y = self.tiledims[0] * i, self.tiledims[1] * j
            img_id = self.create_image(x, y, image=image, anchor='nw', tag='img')
            self.id_name_map[img_id] = name
            self.id_rank_map[img_id] = self.rank_map[(x,y)]
            images.append(image)
            i+=1
            if ((i % (self.w // self.tiledims[0])) == 0) and (i!=0):
                j+=1
                i=0

        self.tag_bind("img", "<Button-1>", self.onClick1)
        self.tag_bind("img", "<B1-Motion>", self.onMotion1)
        self.tag_bind("img", "<ButtonRelease-1>", self.onRelease1)

    def _get_rank_map(self):
        positions = list()
        nrows, ncols = self.w // self.tiledims[0], self.h // self.tiledims[1]
        nrows += 10; ncols += 10
        for i in range(nrows):
            for j in range(ncols):
                positions.append((j*self.tiledims[0], i*self.tiledims[1]))
        return dict(zip(positions, range(nrows * ncols)))

    def _cmpkeys(self, key):
        return self.id_rank_map[key]

    def getSortedNames(self):
        tkids = list(self.id_rank_map.keys())
        tkids.sort(key=self._cmpkeys)
        return [self.id_name_map[tkid] for tkid in tkids]

    def _get_snapping_point(self, pnt):
        x = round(pnt[0]//self.tiledims[0])*self.tiledims[0]
        y = round(pnt[1]//self.tiledims[1])*self.tiledims[1]
        return (x,y)

    def onClick1(self, event):
        self.click = event.x, event.y
        self.click_id = self.find_overlapping(event.x, event.y, event.x, event.y) [0]
        self.click_snaploc = self._get_snapping_point(self.click)

        for listener in self.listeners:
            listener.notify(self.id_name_map[self.click_id])

    def onMotion1(self, event):
        x, y = self.click
        dx = event.x - x
        dy = event.y - y
        self.move('current' ,dx ,dy)
        self.click = event.x, event.y

    def onRelease1(self, event):
        x, y = self._get_snapping_point(self.click)

        if self.rank_map[x, y] not in list(self.id_rank_map.values()):
            self.coords(self.click_id, x, y)
            self.id_rank_map[self.click_id] = self.rank_map[x,y]
        else:
            self.coords(self.click_id, self.click_snaploc[0], self.click_snaploc[1])

        print(self.id_name_map[self.click_id], self.id_rank_map[self.click_id])

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('1200x900')

    with open('linkfile.txt') as lf:
        all_names, links = parse_linkfile(lf)
        link_dict = dict(zip(all_names, links))

    names = ["Kirari Moroboshi", "Shimamu", "Mio Honda", "Yoshiko Tsushima",
            "Kirari Moroboshi", "Shimamu", "Mio Honda", "Yoshiko Tsushima",
            "Kirari Moroboshi", "Shimamu", "Mio Honda", "Yoshiko Tsushima"]

    sorting_grid = SortingGrid(root, (63, 98), width=1200, height=900,
                                link_dict=link_dict, names=names)

    sorting_grid.pack()
    button = tk.Button(root, text="print rankmap", command= lambda: print(sorting_grid.getSortedNames()))
    button.pack()
    root.mainloop()