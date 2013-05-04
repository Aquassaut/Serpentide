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

        # lets see if it's in the continuity of the last segment

        if self.segs == []:
            x = X - 25
            y = Y
            walkable = True
            pointAlreadyUsed = False
        else:
            x, y = self.segs[-1].getEndPoint()
            walkable = fabs(x - X) == 25 and not fabs(y - Y) == 25
            walkable = walkable or fabs(y - Y) == 25 and not fabs(x - X) == 25
        #let's see if it's auto avoiding
            pointAlreadyUsed = self.segs[0].getStartPoint() == (X, Y)
            for seg in self.segs:
                pointAlreadyUsed = pointAlreadyUsed or seg.getEndPoint() == (X, Y)

        #if everything is OK
        if walkable and not pointAlreadyUsed:
            if x == X:
                if Y < y:
                    dct = 3
                else:
                    dct = 1
            else:
                if X > x:
                    dct = 0
                else:
                    dct = 2

            seg = Segment(x, y, dct)
            self.segs.append(seg)
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
        if not self.helpShown:
            self.showHelp()
        circle = self.findInter(event.x, event.y)
        if circle:
            print (event.x, event.y)
            self.requestSeg(circle)

    def findInter(self, x, y):
        items = self.can.find_overlapping(x, y, x, y)
        for item in items:
            if item in self.helpCircles:
                return item
        return False

    def swipeEnd(self, event):
        if self.helpShown:
            self.hideHelp()

    def click(self, event):
        if not self.helpShown:
            self.showHelp()

    def walkable(self, x, y):
        #il faut que
        testx, testy = self.segs[-1].getEndPoint()
        #testx soit 25 px plus loin ET que testy soit le meme OU
        #testx soit le meme ET testy soit 25px plus loin, PAS EN MEME TEMPS
        hor = fabs(testx - x) - SSIZE < TOL and fabs(testy - y) < TOL
        ver = fabs(testy - y) - SSIZE < TOL and fabs(testx - x) < TOL
        return (hor and not ver) or (ver and not hor)
