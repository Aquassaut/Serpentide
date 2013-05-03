from Tkinter import *
from constants import *


class GridCanvas:

    def __init__(self, root):
        self.segs = []
        self.can = Canvas(root, bg=CBG, height=GSIZE, width=GSIZE)
        self.can.bind("<Button-1>", self.click)
        self.can.pack(side=LEFT)
        self.drawGrid()

    def drawGrid(self):
        for div in range(25):
            sec = 25*div
            self.can.create_line(0, sec, GSIZE, sec, width=2, fill=GFILL)
            self.can.create_line(sec, 0, sec, GSIZE, width=2, fill=GFILL)

    def click(self, event):
        #TEST
        print "C'est un clic !"
        print str(event)
