import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi


class TableWidget(QWidget):

    def __init__(self, uipath):
        super().__init__()
        self.uiPath = uipath
        self.tableView = None

        self.initUI()
        self.initHeaderHorizontal()
        self.initHeaderVertical()

    def initUI(self):
        self.ui = loadUi(self.uiPath, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter,
                                            self.size(), QApplication.desktop().availableGeometry()))
        self.show()

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
        self.saveShortcut = QShortcut(QKeySequence("Ctrl+S"), self)

    def test(self):
        for i in range(8, 20):
            self.tableView.model().cs.addCar(i, "foo{0}".format(i), 20)
            self.tableView.model().cs.appendLapTime(i, 91, 0, 0, 0)
            print(self.tableView.model().columnCount(None))
            self.tableView.repaint()
        for i in range(1, 20):
            self.tableView.model().cs.appendLapTime(5, i, 0, 0, 0)
