from Parser import *


class test:

    def __init__(self):
        self.p = Parser()

    def seqRead(self):
        print("Please enter a sequence")
        liste = self.p.readFromInput()
        print liste
        return liste

    def seqWrite(self):
        seq = self.p.toSequence(self.seqRead())
        print seq

test().seqWrite()
