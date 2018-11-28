
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


from src.graph.LeaderBoardWidget import *


class LeaderBoard():

    def __init__(self, uipath):
        self.uiPath = uipath
        self.widget = None
        self.dataStorage = None

        self.initWidget()

    def initWidget(self):
        self.widget = LeaderBoardWidget()
        self.widget.initUI(self.uiPath)

    def getWidget(self):
        return self.widget

    def updateData(self, data):
        self.dataStorage = data