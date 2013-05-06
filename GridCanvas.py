from Tkinter import *
from constants import *
from Segment import *
from math import fabs


class GridCanvas:

    segs = []
    helpCircles = []
    can = None
    helpShown = False
    firstCoords = None
    allowSelfAvoidOnly = True
    lead = None

    def __init__(self, root):
        self.segs = []
        self.can = Canvas(root, bg=CBG, height=GSIZE, width=GSIZE)
        self.can.pack(expand=YES, side=LEFT)
        self.drawHelp()
        self.drawGrid()
        self.can.bind("<Button-1>", self.click)
        self.can.bind("<B1-Motion>", self.swipe)
        self.can.bind("<ButtonRelease-1>", self.swipeEnd)
        self.can.bind("<Up>", self.upKey)
        self.can.bind("<Down>", self.downKey)
        self.can.bind("<Left>", self.leftKey)
        self.can.bind("<Right>", self.rightKey)
        self.can.bind("<Control-z>", self.cancel)
        self.can.bind(LCAM, self.leftCamKey)
        self.can.bind(RCAM, self.rightCamKey)
        self.can.bind(UCAM, self.upCamKey)
        self.can.bind(DCAM, self.downCamKey)
        self.lead = self.can.create_oval(MIDDLE - 3, MIDDLE - 3, MIDDLE + 3, MIDDLE + 3, fill=LFILL)

    def drawGrid(self):
        for div in range(NBCELL):
            sec = SSIZE*div
            self.can.create_line(0, sec, GSIZE, sec, width=3, fill=GFILL)
            self.can.create_line(sec, 0, sec, GSIZE, width=3, fill=GFILL)

    def drawHelp(self):
        self.helpCircles = []
        for hor in range(1, NBCELL):
            for ver in range(1, NBCELL):
                x = SSIZE*hor
                y = SSIZE*ver
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
        self.firstCoords = None
        self.moveLead(MIDDLE, MIDDLE)
        for seg in self.segs:
            self.can.delete(seg.getGraphicObject())
            seg.rmGraphicObject()
        self.segs = segments
        self.redrawSegs()

    def moveLead(self, x, y):
        self.can.coords(self.lead, x - 3, y - 3, x + 3, y + 3)

    def segRequest(self, x, y, X, Y, dct=None):
        free = self.freePoint(X, Y)
        if (not free) or (not self.allowSelfAvoidOnly):
            # segment backtrack
            if self.counterSeg(x, y, X, Y):
                if len(self.segs) > 0:
                    self.moveLead(X, Y)
                else:
                    leadX, leadY = self.segs[-1].getStartPoint()
                    self.moveLead(leadX, leadY)
                self.eraseLastSeg()
                return
        if free:
            if dct is None:
                dct = self.findDct(x, y, X, Y)
            seg = Segment(x, y, dct)
            self.segs.append(seg)
            self.drawSeg(seg, SFILL)
            self.moveLead(X, Y)

    def requestSegByCircle(self, circle):
        Xa, Ya, Xb, Yb = self.can.coords(circle)
        X = (Xa + Xb)/2
        Y = (Ya + Yb)/2
        if self.segs == []:
            if self.firstCoords is not None:
                x, y = self.firstCoords
            else:
                self.firstCoords = (X, Y)
                self.moveLead(X, Y)
                return
        else:
            x, y = self.segs[-1].getEndPoint()
        cont = self.continuous(x, y, X, Y)
        if cont:
            self.segRequest(x, y, X, Y)

    def requestSegByDct(self, dct):
        if self.segs == []:
            x, y = MIDDLE, MIDDLE
        else:
            x, y = self.segs[-1].getEndPoint()
        X, Y = {
            0: (x + SSIZE, y),
            1: (x, y + SSIZE),
            2: (x - SSIZE, y),
            3: (x, y - SSIZE),
        }[dct]
        self.segRequest(x, y, X, Y, dct)

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

    def counterSeg(self, x, y, X, Y):
        if self.segs == []:
            return False
        st = self.segs[-1].getStartPoint()
        end = self.segs[-1].getEndPoint()
        return st == (X, Y) and end == (x, y)

    def freePoint(self, X, Y):
        if X < 0 or Y < 0 or X > GSIZE or Y > GSIZE:
            return False
        if not self.allowSelfAvoidOnly:
            return True
        if self.segs == []:
            return True
        if self.segs[0].getStartPoint() == (X, Y):
            return False
        for seg in self.segs:
            if seg.getEndPoint() == (X, Y):
                return False
        return True

    def continuous(self, x, y, X, Y):
        hor = fabs(x - X) == SSIZE and y == Y
        ver = fabs(y - Y) == SSIZE and x == X
        return (hor and not ver) or (ver and not hor)

    def drawSeg(self, seg, sfill=SFILL):
        x, y = seg.getStartPoint()
        X, Y = seg.getEndPoint()
        go = self.can.create_line(x, y, X, Y, width=3, fill=sfill)
        seg.addGraphicObject(go)

    def eraseLastSeg(self):
        self.can.delete(self.segs.pop().getGraphicObject())

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
            self.requestSegByCircle(circle)

    def swipeEnd(self, event):
        if self.helpShown:
            self.hideHelp()

    def click(self, event):
        self.can.focus_force()
        if self.segs == []:
            startCircle = self.findInter(event.x, event.y)
            if startCircle:
                xa, ya, xb, yb = self.can.coords(startCircle)
                self.firstCoords = ((xa + xb)/2, (ya + yb)/2)
        if not self.helpShown:
            self.showHelp()

    def moveAllSeg(self, dct, amount=1):
        dy = 0
        dx = 0
        if dct == 0:
            dx = 1
        elif dct == 2:
            dx = -1
        elif dct == 1:
            dy = 1
        else:
            dy = -1
        dx = dx * amount * SSIZE
        dy = dy * amount * SSIZE
        for seg in self.segs:
            seg.move(dx, dy)
        self.wipe(self.segs)

    def leftKey(self, event):
        self.requestSegByDct(2)

    def downKey(self, event):
        self.requestSegByDct(1)

    def rightKey(self, event):
        self.requestSegByDct(0)

    def upKey(self, event):
        self.requestSegByDct(3)

    def leftCamKey(self, event):
        self.moveAllSeg(2)

    def downCamKey(self, event):
        self.moveAllSeg(1)

    def rightCamKey(self, event):
        self.moveAllSeg(0)

    def upCamKey(self, event):
        self.moveAllSeg(3)

    def cancel(self, event):
        if not self.segs == []:
            self.requestSegByDct((self.segs[-1].getDct() + 2) % 4)
