from Tkinter import *
from constants import *
from Segment import *
from math import fabs


class GridCanvas:

    segs = []
    helpCircles = []
    can = None
    helpShown = False

    def __init__(self, root):
        self.segs = []
        self.can = Canvas(root, bg=CBG, height=GSIZE, width=GSIZE)
        self.can.pack(side=LEFT)
        self.drawHelp()
        self.drawGrid()
        self.can.bind("<Button-1>", self.click)
        self.can.bind("<B1-Motion>", self.swipe)
        self.can.bind("<ButtonRelease-1>", self.swipeEnd)

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
                temp = self.can.create_oval(x - CR, y - CR, x + CR, y + CR, **HCOPT)
                self.helpCircles.append(temp)

    def hideHelp(self):
        for circle in self.helpCircles:
            self.can.itemconfig(circle, **HCOPT)
        self.helpShown = False

    def showHelp(self):
        for circle in self.helpCircles:
            self.can.itemconfig(circle, **SCOPT)
        self.helpShown = True

    def wipe(self, segments):
        for seg in self.segs:
            self.can.delete(seg.getGraphicObject())
            seg.rmGraphicObject()
        self.segs = segments
        self.redrawSegs()

    def requestSeg(self, circle):
        Xa, Ya, Xb, Yb = self.can.coords(circle)
        X = (Xa + Xb)/2
        Y = (Ya + Yb)/2
        if self.segs == []:
            x, y = X - 25, Y
            free = cont = True
        else:
            x, y = self.segs[-1].getEndPoint()
            cont = self.continuous(x, y, X, Y)
            free = self.freePoint(X, Y)
        if cont and free:
            seg = Segment(x, y, dct)
            self.segs.append(seg)
            self.drawSeg(self.segs[-1])

    def findDct(self, x, y, X, Y):
        if x == X:
            if Y < y:
                return 3
            else:
                return 1
        else:
            if X > x:
                return 0
            else:
                return 2

    def freePoint(self, X, Y):
        if self.segs[0].getStartPoint() == (X, Y):
            return False
        for seg in self.segs:
            if seg.getEndPoint() == (X, Y):
                return False
        return True

    def continuous(self, x, y, X, Y):
        if self.segs == []:
            return True
        else:
            hor = fabs(x - X) == 25
            ver = fabs(y - Y) == 25
            return (hor and not ver) or (ver and not hor)

    def drawSeg(self, seg):
        x, y = seg.getStartPoint()
        X, Y = seg.getEndPoint()
        go = self.can.create_line(x, y, X, Y, width=3, fill=SFILL)
        seg.addGraphicObject(go)

    def redrawSegs(self):
        for seg in self.segs:
            self.drawSeg(seg)

    def findInter(self, x, y):
        items = self.can.find_overlapping(x, y, x, y)
        for item in items:
            if item in self.helpCircles:
                return item
        return False

    def swipe(self, event):
        if not self.helpShown:
            self.showHelp()
        circle = self.findInter(event.x, event.y)
        if circle:
            print (event.x, event.y)
            self.requestSeg(circle)

    def swipeEnd(self, event):
        if self.helpShown:
            self.hideHelp()

    def click(self, event):
        if not self.helpShown:
            self.showHelp()
