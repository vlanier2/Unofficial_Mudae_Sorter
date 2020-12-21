from io import BytesIO
import requests
from PIL import ImageTk, Image
'''
utilities.py
Just some helper functions
'''

def parse_linkfile(openfile):
    names = list()
    links = list()
    
    line = openfile.readline()
    while line:
        line = line.rstrip()
        if line == '': pass
        else:
            split_line = line.rsplit('-', 1)
            names.append(split_line[0].strip())
            links.append(split_line[1].strip())
        line = openfile.readline()
    return names, links

def get_recently_appended(textin):
    return [substr.rsplit('-', 1)[0].strip() for substr in textin.split('\n') if substr != '']

def img_from_url(url, size=(69,69)):
    img = Image.open(BytesIO(requests.get(url).content))
    img = ImageTk.PhotoImage(img.resize(size))
    return img

def get_url_dict(img_dict, name):
    return img_dict[name]