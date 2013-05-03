from Tkinter import *
from tkFileDialog import askopenfilename
from Segment import *
from Parser import *
from GridCanvas import *
from constants import *


class App:

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
        filemenu.add_command(label="New")
        filemenu.add_command(label="Open...", command=self.openFile)
        filemenu.add_command(label="Save")
        filemenu.add_command(label="Save as...")
        filemenu.add_command(label="Quit", command=root.quit)
        return filemenu

    def openFile(self):
        filename = self.getFileDialog()
        received = Parser().readFromFile(filename)
        #TEST
        print received

    def getFileDialog(self):
        return askopenfilename(filetypes=[("All file types", "*")])


root = Tk()
app = App(root)
root.mainloop()
