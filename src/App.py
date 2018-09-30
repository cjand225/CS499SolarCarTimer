import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

from Table import *

class AppWindow(QMainWindow):

    def __init__(self):
        super(AppWindow, self).__init__()
        self.initMainWindow()
        self.createPopupMenu()
        self.handleTableWidget()
        self.initUI()

    def initMainWindow(self):
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Main Window")
        self.resize(1200,800)

    def initUI(self):
        self.setCentralWidget(self.mTable)
        self.show()

    def handleTableWidget(self):
        self.mTable = Table()

    #def handleButtonWidget(self):
    #def handleVisionWidget(self):
