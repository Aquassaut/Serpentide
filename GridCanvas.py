from Tkinter import *
from constants import *
from Segment import *
from math import floor, fabs


class GridCanvas:

    def __init__(self, root):
        self.segs = []
        self.can = Canvas(root, bg=CBG, height=GSIZE, width=GSIZE)
        self.can.bind("<Button-1>", self.click)
        self.can.bind("<Button1-Motion>", self.swipe)
        self.can.pack(side=LEFT)
        self.drawGrid()

    def drawGrid(self):
        for div in range(NBCELL):
            sec = NBCELL*div
            self.can.create_line(0, sec, GSIZE, sec, width=3, fill=GFILL)
            self.can.create_line(sec, 0, sec, GSIZE, width=3, fill=GFILL)

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
        print "C'est un deplacement !"
        print str(event.x), str(event.y)

    def click(self, event):
        if self.segs == []:
            self.newSeg(Segment(SIZE*event.x/SSIZE, SIZE*event.y/SSIZE, 1))
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
        print "C'est un clic !"
        print str(event.x), str(event.y)

    def walkable(self, x, y):
        #il faut que
        testx, testy = self.segs[-1].getEndPoint()
        #testx soit 25 px plus loin ET que testy soit le meme OU
        hor = fabs(testx - x) - SSIZE < TOL and fabs(testy - y) < TOL
        #testx soit le meme ET testy soit 25px plus loin, PAS EN MEME TEMPS
        ver = fabs(testy - y) - SSIZE < TOL and fabs(testx - x) < TOL
        return (hor and not ver) or (ver and not hor)
