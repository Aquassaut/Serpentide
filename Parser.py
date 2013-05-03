import Segment


class Parser:
    """ Parses and creates segment from direction sequences"""

    def __init__(self):
        pass

    def toSegments(self, sequence):
        position = (0, 0)
        seqList = []
        for segment in sequence:
            temp = Segment.Segment(position[0], position[1], int(segment))
            position = temp.getEndPoint()
            seqList.append(temp)
        return seqList

    def toSequence(self, segments):
        sequence = ""
        for seg in segments:
            sequence += str(seg.getDct())
        return sequence

    def readFromInput(self):
        sequence = raw_input()
        return self.toSegments(sequence)

    def readFromFile(self, filename):
        file = open(filename)
        fileData = file.read()
        file.close()
        return self.toSegments(fileData)

    def writeToFile(self, segments, filename):
        seq = self.toSequence(segments)
        file = open(filename, "w")
        file.write(seq)
        file.close()
