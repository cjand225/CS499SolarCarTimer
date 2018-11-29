
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import os

from src.graph.LeaderBoardWidget import *


class LeaderBoard():
    resourcesDir = os.path.abspath(os.path.join(__file__, "./../../../resources"))
    LeaderBoardUIPath = os.path.join(resourcesDir, 'LeaderBoard.ui')

    def __init__(self):
        self.widget = None
        self.dataStorage = None

        self.initWidget()

    def initWidget(self):
        self.widget = LeaderBoardWidget(self.LeaderBoardUIPath)

    def getWidget(self):
        return self.widget

    def updateData(self, data):
        self.dataStorage = data
        #self.widget.tableView.setModel(self.dataStorage)

