from constants import *


class Segment:
    """ Defines a segment with a length of 1 according
    to its starting point and its direction """

    def __init__(self, x, y, dct):
        assert dct <= 3 and dct >= 0
        self.x = x
        self.y = y
        self.dct = dct

    def move(self, dx, dy):
        """moves a segment by a given offset"""
        self.x += dx
        self.y += dy

    def getEndPoint(self):
        """returns the ending point of the segment in a tuple"""
        return {
            0: (self.x + SSIZE, self.y),
            1: (self.x, self.y + SSIZE),
            2: (self.x - SSIZE, self.y),
            3: (self.x, self.y - SSIZE),
        }[self.dct]

    def getStartPoint(self):
        """returns the starting point of the segment in a tuple"""
        return (self.x, self.y)

    def getDct(self):
        return self.dct

    def addGraphicObject(self, go):
        self.go = go

    def getGraphicObject(self):
        return self.go

    def rmGraphicObject(self):
        self.go = None