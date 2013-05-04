from Tkinter import *
from constants import *
from Segment import *
from math import floor, fabs


class GridCanvas:

    segs = []
    helpCircles = []
    can = None

    def __init__(self, root):
        self.segs = []
        self.can = Canvas(root, bg=CBG, height=GSIZE, width=GSIZE)
        self.can.bind("<Button-1>", self.click)
        self.can.bind("<B1-Motion>", self.swipe)
        self.can.bind("<ButtonRelease-1>", self.swipeEnd)
        self.can.pack(side=LEFT)
        self.drawGrid()
        self.drawHelp()

    def drawGrid(self):
        for div in range(NBCELL):
            sec = NBCELL*div
            self.can.create_line(0, sec, GSIZE, sec, width=3, fill=GFILL)
            self.can.create_line(sec, 0, sec, GSIZE, width=3, fill=GFILL)

    def drawHelp(self):
        self.helpCircles = []
        for hor in range(1, NBCELL):
            for ver in range(1, NBCELL):
                x = NBCELL*hor
                y = NBCELL*ver
                temp = self.can.create_oval(x - 8, y - 8, x + 8, y + 8, fill="brown", stipple="gray12")
                self.helpCircles.append(temp)

    def wipe(self, segments):
        for seg in self.segs:
            self.can.delete(seg.getGraphicObject())
            seg.rmGraphicObject()
        self.segs = segments
        self.redrawSegs()

    def newSeg(self, segment):
        self.segs.append(segment)
        self.drawSeg(self.segs[-1])

    def drawSeg(self, seg):
        x, y = seg.getStartPoint()
        X, Y = seg.getEndPoint()
        go = self.can.create_line(x, y, X, Y, width=3, fill=SFILL)
        seg.addGraphicObject(go)

    def redrawSegs(self):
        for seg in self.segs:
            self.drawSeg(seg)

    def swipe(self, event):
        pass

    def swipeEnd(self, event):
        pass

    def click(self, event):
        if self.segs == []:

            self.newSeg(Segment(SSIZE*(event.x/SSIZE), SSIZE*(event.y/SSIZE), 1))
        elif self.walkable(event.x, event.y):
            x, y = self.segs[-1].getEndPoint()
            if fabs(event.x - x) < TOL:
                if event.y < y:
                    dct = 3
                else:
                    dct = 1
            else:
                if event.x > x:
                    dct = 2
                else:
                    dct = 0
            print dct
            self.newSeg(Segment(x, y, dct))

    def walkable(self, x, y):
        #il faut que
        testx, testy = self.segs[-1].getEndPoint()
        #testx soit 25 px plus loin ET que testy soit le meme OU
        hor = fabs(testx - x) - SSIZE < TOL and fabs(testy - y) < TOL
        #testx soit le meme ET testy soit 25px plus loin, PAS EN MEME TEMPS
        ver = fabs(testy - y) - SSIZE < TOL and fabs(testx - x) < TOL
        return (hor and not ver) or (ver and not hor)
