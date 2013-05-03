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
        """return the ending point of the segment in a tuple"""
        return {
            0: (self.x + 1, self.y),
            1: (self.x, self.y - 1),
            2: (self.x - 1, self.y),
            3: (self.x, self.y + 1),
        }[self.dct]

    def getDct(self):
        return self.dct
