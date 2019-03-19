"""

    Module:
    Purpose:
    Depends On:

"""

from PyQt5.QtWidgets import QWidget, QApplication, QHeaderView, QShortcut, QStyle
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi

from SCTimeUtility.Log.Log import getLog


class TableWidget(QWidget):

    def __init__(self, uipath):
        super().__init__()
        self.uiPath = uipath
        self.tableView = None

        self.initUI()
        self.saveShortcut = QShortcut(QKeySequence("Ctrl+S"), self)

    '''
        Function: initUI
        Parameters: self
        Return Value: N/A
        Purpose: Initializes the GUI for TableWidget by loading its' resource file, storing a reference to it 
                 in self.UI
                 
    '''

    def initUI(self):
        self.ui = loadUi(self.uiPath, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter,
                                            self.size(), QApplication.desktop().availableGeometry()))
        self.show()

    '''
        Function: initHeaderHorizontal
        Parameters: self
        Return Value: N/A
        Purpose: Initializes the horizontal headers for the Table view widget, such that it has
                 proper spacing for items its displaying

    '''

    def initHeaderHorizontal(self):
        # Resizes the horizontal header so that the Table fits initially without scrollbars.
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for headerIndex in range(len(self.tableView.horizontalHeader())):
            # sectionSize computes the width of the column header.
            # As a side effect, it also forces the header to resize to f it its container.
            self.tableView.horizontalHeader().sectionSize(headerIndex)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)

    '''
        Function: iniHeaderVertical
        Parameters: self
        Return Value: N/A
        Purpose: Initializes the vertical headers for the Table view widget, such that it has
                 proper spacing for items its displaying

    '''

    def initHeaderVertical(self):
        # Resizes the vertical header so that the Table fits initially without scrollbars.
        self.tableView.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for headerIndex in range(len(self.tableView.verticalHeader())):
            # sectionSize computes the height of the row header.
            # As a side effect, it also forces the header to resize to fit its container.
            self.tableView.verticalHeader().sectionSize(headerIndex)
        self.tableView.verticalHeader().setSectionResizeMode(QHeaderView.Interactive)

    '''
        Function: test
        Parameters: self
        Return Value: N/A
        Purpose: Populates TableView with some dummy data to test if its properly displaying content.

    '''

    def test(self):
        for i in range(8, 20):
            self.tableView.model().cs.addCar(i, "foo{0}".format(i), 20)
            self.tableView.model().cs.appendLapTime(i, 91, 0, 0, 0)
            print(self.tableView.model().columnCount(None))
            self.tableView.repaint()
        for i in range(1, 20):
            self.tableView.model().cs.appendLapTime(5, i, 0, 0, 0)
