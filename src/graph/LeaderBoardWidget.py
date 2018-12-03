from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
from PyQt5.Qt import *
from src.log.Log import getInfoLog, getCriticalLog, getDebugLog, getErrorLog, getWarningLog


class LeaderBoardWidget(QWidget):

    def __init__(self, uiPath):
        super().__init__()
        self.ui = None
        self.uiPath = uiPath

        self.initUI()

    def initUI(self):
        self.ui = loadUi(self.uiPath, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(), QApplication.desktop().availableGeometry()))
    def resizeEvent(self, a0: QResizeEvent):
        self.initHeaderHorizontal()
        self.initHeaderVertical()

    def initHeaderHorizontal(self):
        minSize = 0
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for headerIndex in range(len(self.tableView.horizontalHeader())):
            minSize = min(minSize, self.tableView.horizontalHeader().sectionSize(headerIndex))
        self.tableView.horizontalHeader().setMinimumSectionSize(minSize)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)

    def initHeaderVertical(self):
        minSize = 0
        self.tableView.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for headerIndex in range(len(self.tableView.verticalHeader())):
            minSize = min(minSize, self.tableView.verticalHeader().sectionSize(headerIndex))
        self.tableView.verticalHeader().setMinimumSectionSize(minSize)
        self.tableView.verticalHeader().setSectionResizeMode(QHeaderView.Interactive)
