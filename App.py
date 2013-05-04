from Tkinter import *
from tkFileDialog import askopenfilename, asksaveasfilename
from Segment import *
from Parser import *
from GridCanvas import *
from constants import *


class App:

    currentFile = None

    def __init__(self, root):
        root.minsize(ASIZE, ASIZE)
        self.drawMenu(root)
        self.can = GridCanvas(root)

    def drawMenu(self, root):
        menuBar = Menu(root)
        menuBar.add_cascade(label="File", menu=self.drawFileMenu(menuBar))
        root.config(menu=menuBar)

    def drawFileMenu(self, menuBar):
        filemenu = Menu(menuBar, tearoff=0)
        filemenu.add_command(label="New", command=self.new)
        filemenu.add_command(label="Open...", command=self.openFile)
        filemenu.add_command(label="Save", command=self.save)
        filemenu.add_command(label="Save as...", command=self.saveAs)
        filemenu.add_command(label="Debug", command=self.debug)
        filemenu.add_command(label="Quit", command=root.quit)
        return filemenu

    def saveAs(self):
        filename = self.getSaveDialog()
        if filename:
            self.currentFile = filename
            Parser().writeToFile(self.can.segs, filename)

    def save(self):
        if self.currentFile is None:
            return self.saveAs()
        else:
            Parser().writeToFile(self.can.segs, self.currentFile)

    def new(self):
        self.currentFile = None
        self.can.wipe([])

    def debug(self):
        print Parser().toSequence(self.can.segs)

    def openFile(self):
        filename = self.getOpenDialog()
        received = Parser().readFromFile(filename)
        self.can.wipe(received)

    def getSaveDialog(self):
        sFOPT = FOPT
        sFOPT["initialfile"] = "new walk.spw"
        return asksaveasfilename(**FOPT)

    def getOpenDialog(self):
        return askopenfilename(**FOPT)


root = Tk()
app = App(root)
root.mainloop()
