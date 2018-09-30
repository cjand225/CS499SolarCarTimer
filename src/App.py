import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

from Table import *

class AppWindow(QMainWindow):

    def __init__(self):
        super(AppWindow, self).__init__()
        self.initMainWindow()
        self.createPopupMenu()
        self.initMainMenu()
        self.handleTableWidget()
        self.initUI()

    def initMainWindow(self):
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Main Window")
        self.resize(1200,800)


    def initMainMenu(self):
        mBar = self.menuBar()
        self.fileMenu = mBar.addMenu("File")    #Menu
        self.fileMenu.addAction("New")          #Item of Submenu File
        self.fileMenu.addAction("Open")         #Item of Submenu File
        self.fileMenu.addAction("Export")       #Item of Submenu File
        self.fileMenu.addAction("Quit")         #Item of Submenu File

        self.editMenu = mBar.addMenu("Edit")    #Menu
        self.editMenu.addAction("Cut")          #Item of Submenu Edit
        self.editMenu.addAction("Copy")         #Item of Submenu Edit
        self.editMenu.addAction("Paste")        #Item of Submenu Edit

        self.viewMenu = mBar.addMenu("View")    #Menu
        self.viewMenu.addAction("Semi-Auto")    #Item of Submenu View
        self.viewMenu.addAction("Auto")         #Item of Submenu View

        self.helpMenu = mBar.addMenu("Help")    #Menu
        self.helpMenu.addAction("About")        #Item of Submenu Help

        # save = QAction("Save", self)
        # save.setShortcut("Ctrl+S")
        # self.fileMenu.addAction(save)

        #set Bindings from QActions to relevant functions
        self.fileMenu.triggered[QAction].connect(self.fileTrigger)

    #debug function for bindings
    def fileTrigger(self, q):
        print(" is triggered")

    #Initalize/show ui components here
    def initUI(self):
        self.show()

    #handles TableWidget stuff
    def handleTableWidget(self):
        self.mTable = Table()
        self.setCentralWidget(self.mTable)

    #def handleButtonWidget(self):
    #def handleVisionWidget(self):
