import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
from src.log.Log import getInfoLog, getCriticalLog, getDebugLog, getErrorLog, getWarningLog


class TableWidget(QWidget):

    def __init__(self, uipath):
        super().__init__()
        self.uiPath = uipath
        self.tableView = None

        self.initUI()
        self.saveShortcut = QShortcut(QKeySequence("Ctrl+S"), self)


    def initUI(self):
        self.ui = loadUi(self.uiPath, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter,
                                            self.size(), QApplication.desktop().availableGeometry()))
        self.show()



    def initHeaderHorizontal(self):
        # Resizes the horizontal header so that the table fits initially without scrollbars.
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for headerIndex in range(len(self.tableView.horizontalHeader())):
            # sectionSize computes the width of the column header.
            # As a side effect, it also forces the header to resize to f it its container.
            self.tableView.horizontalHeader().sectionSize(headerIndex)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        

    def initHeaderVertical(self):
        # Resizes the vertical header so that the table fits initially without scrollbars.
        self.tableView.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for headerIndex in range(len(self.tableView.verticalHeader())):
            # sectionSize computes the height of the row header.
            # As a side effect, it also forces the header to resize to fit its container.
            self.tableView.verticalHeader().sectionSize(headerIndex)
        self.tableView.verticalHeader().setSectionResizeMode(QHeaderView.Interactive)

    def test(self):
        for i in range(8, 20):
            self.tableView.model().cs.addCar(i, "foo{0}".format(i), 20)
            self.tableView.model().cs.appendLapTime(i, 91, 0, 0, 0)
            print(self.tableView.model().columnCount(None))
            self.tableView.repaint()
        for i in range(1, 20):
            self.tableView.model().cs.appendLapTime(5, i, 0, 0, 0)
