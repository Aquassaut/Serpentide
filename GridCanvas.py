from Tkinter import *
from constants import *
from Segment import *
from math import fabs, pi


class GridCanvas:

    segs = []
    helpCircles = []
    can = None
    helpShown = False
    firstCoords = None
    # allowSelfAvoidOnly is an option activated by default (can be deactivated
    # by the user in the GUI) which forbid segments collisions.
    allowSelfAvoidOnly = True
    lead = None

    # dct is the segment direction :
    #   up -> 3
    #   down -> 1
    #   right -> 0
    #   left -> 2

    def __init__(self, root):
        self.segs = []
        self.can = Canvas(root, bg=CBG, height=GSIZE, width=GSIZE)
        self.can.pack(expand=YES, side=LEFT)
        self.drawHelp()
        self.drawGrid()

        # Print help, add or remove segments with the mouse
        self.can.bind("<Button-1>", self.click)
        self.can.bind("<B1-Motion>", self.swipe)
        self.can.bind("<ButtonRelease-1>", self.swipeEnd)

        # Add or remove segments with the keyboard arrows
        for key in ["<Up>", "<Down>", "<Left>", "<Right>"]:
            self.can.bind(key, self.keyMove)

        # Move the draw on the screen. Keybinds :
        #   "q": left
        #   "d": right
        #   "z": up
        #   "s": down
        for key in ["q", "d", "z", "s"]:
            self.can.bind(key, self.keyCam)

        # Launch undo
        self.can.bind("<Control-z>", self.undo)
        # Launch segments rotations around the double clicked point
        self.can.bind("<Double-Button-1>", self.doubleClick)

        self.lead = self.can.create_oval(MIDDLE - 3, MIDDLE - 3, MIDDLE + 3, MIDDLE + 3, fill=LFILL)

        # Necessary to avoid clicking on the window/grid at start
        self.can.focus_force()

    def drawGrid(self):
        """ Draws the grid on which the segment are gonna be bound """
        for div in range(NBCELL):
            sec = SSIZE*div
            self.can.create_line(0, sec, GSIZE, sec, width=3, fill=GFILL)
            self.can.create_line(sec, 0, sec, GSIZE, width=3, fill=GFILL)

    def drawHelp(self):
        """ Draw circles on each cross on the grid to help the user """
        self.helpCircles = []
        for hor in range(1, NBCELL):
            for ver in range(1, NBCELL):
                x = SSIZE*hor
                y = SSIZE*ver
                temp = self.can.create_oval(x - CR, y - CR, x + CR, y + CR, **HCOPT)
                self.helpCircles.append(temp)

    def hideHelp(self):
        """ Hide the circles (help) """
        for circle in self.helpCircles:
            self.can.itemconfig(circle, **HCOPT)
        self.helpShown = False

    def showHelp(self):
        """ Show the circles (help) """
        for circle in self.helpCircles:
            self.can.itemconfig(circle, **SCOPT)
        self.helpShown = True

    def wipe(self, segments):
        """ Clean the segments and redraw the walk given in parameter """
        self.firstCoords = None
        self.moveLead(MIDDLE, MIDDLE)
        for seg in self.segs:
            self.can.delete(seg.getGraphicObject())
            seg.rmGraphicObject()
        self.segs = segments
        self.redrawSegs()

    def moveLead(self, x, y):
        """ Move the lead on the coordinates given in parameter """
        self.can.coords(self.lead, x - 3, y - 3, x + 3, y + 3)

    def segRequest(self, x, y, X, Y, dct=None):
        """ Create a new segment at the coordinates given in parameter if possible.
            If there is already the last created segment, segRequest() delete it. """
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
        """ Calculates the segment coordinates when it is created with the mouse """
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
        """ Calculates the segment direction when it is created with the keyboard """
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
        """ Return the segment direction """
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
        """ Return segments number between the start point and the end point """
        if self.segs == []:
            return False
        st = self.segs[-1].getStartPoint()
        end = self.segs[-1].getEndPoint()
        return st == (X, Y) and end == (x, y)

    def freePoint(self, X, Y):
        """ Check if it is possible to draw a segment at the cordinated given in
            parameter. """
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
        """ Check if the space between the first point and the second point is
        composed by continuous segments """
        hor = fabs(x - X) == SSIZE and y == Y
        ver = fabs(y - Y) == SSIZE and x == X
        return (hor and not ver) or (ver and not hor)

    def drawSeg(self, seg, sfill=SFILL):
        """ Draw segment(s) from the start point to the end point. """
        x, y = seg.getStartPoint()
        X, Y = seg.getEndPoint()
        go = self.can.create_line(x, y, X, Y, width=3, fill=sfill)
        seg.addGraphicObject(go)

    def eraseLastSeg(self):
        """ Clear the last segment """
        self.can.delete(self.segs.pop().getGraphicObject())

    def redrawSegs(self):
        """ Draw a walk given in parameter """
        for seg in self.segs:
            self.drawSeg(seg)

    def findInter(self, x, y):
        """ Check if the cursor is in a circle (hitbox) :
        yes -> return the circle,
        no -> return false. """
        items = self.can.find_overlapping(x, y, x, y)
        for item in items:
            if item in self.helpCircles:
                return item
        return False

    def swipe(self, event):
        """ Create segments in following the cursor
        (Called when the left mouse button is keeping pressed) """
        if not self.helpShown:
            self.showHelp()
        circle = self.findInter(event.x, event.y)
        if circle:
            self.requestSegByCircle(circle)

    def swipeEnd(self, event):
        """ Hide circles (help)
        (Called when the left mouse button is released) """
        if self.helpShown:
            self.hideHelp()

    def click(self, event):
        """ Show help and initialize the first segment point
        (Called when the left mouse button is pressed) """
        if self.segs == []:
            startCircle = self.findInter(event.x, event.y)
            if startCircle:
                xa, ya, xb, yb = self.can.coords(startCircle)
                self.firstCoords = ((xa + xb)/2, (ya + yb)/2)
        if not self.helpShown:
            self.showHelp()

    def doubleClick(self, event):
        """ Rotates all following segments from the double clicked node
        (Called when the left button is pressed twice) """
        doRotation = False

        self.can.focus_force()
        interCircle = self.findInter(event.x, event.y)
        if interCircle:
            xa, ya, xb, yb = self.can.coords(interCircle)
            inter = ((xa + xb)/2, (ya + yb)/2)
            for seg in self.segs:
                if (not doRotation) and (seg.getStartPoint() == inter):
                    doRotation = True
                    lastInter = inter
                if doRotation:
                    seg.place(lastInter)
                    seg.rotate(pi/2)
                    lastInter = seg.getEndPoint()

            self.wipe(self.segs)

    def moveAllSeg(self, dct, amount=1):
        """ Move all segments in a direction given in parameter """
        dx, dy = {
            0: (amount * SSIZE, 0),
            1: (-amount * SSIZE, 0),
            2: (0, amount * SSIZE),
            3: (0, -amount * SSIZE)
        }[dct]
        for seg in self.segs:
            seg.move(dx, dy)
        self.wipe(self.segs)
        self.moveLead(dx, dy)

    def keyMove(self, event):
        """ Set a direction from the keyboard arrow pressed by the user, and create
            a new segment in this direction """
        UP = 111
        RIGHT = 114
        DOWN = 116
        LEFT = 113
        dct = {
            RIGHT: 0,
            DOWN: 1,
            LEFT: 2,
            UP: 3
        }[event.keycode]
        self.requestSegByDct(dct)

    def keyCam(self, event):
        """ Set a direction from the keyboard arrow pressed by the user, and move
            the map in this direction
                    z : up
            q : left      d : right
                    s : down """
        dct = {
            "d": 0,
            "s": 1,
            "q": 2,
            "z": 3
        }[event.char]
        self.moveAllSeg(dct)

    def undo(self, event=None):
        """ Delete the last segment (uses the fact that creating a segment over the
            last one erase it).
            TODO : make it compatible with rotation """
        if not self.segs == []:
            self.requestSegByDct((self.segs[-1].getDct() + 2) % 4)
