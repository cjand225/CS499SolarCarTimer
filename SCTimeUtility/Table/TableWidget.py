"""

    Module: TableWidget.py
    Purpose: View (front-end) for the table module. Displays spreadsheet like table and controls for
             manipulating car data.
    Depends On: Pyqt, time (python standard lib), SCTimeUtility packages (Log)

"""
import time

from PyQt5.QtWidgets import QWidget, QApplication, QHeaderView, QShortcut, QStyle, QTimeEdit
from PyQt5.QtGui import QKeySequence, QResizeEvent, QPaintEvent, QColor
from PyQt5.QtCore import Qt, QTime
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
        self.lcdTime.setSegmentStyle(2)
        self.timeEdit.setTime(QTime().currentTime())
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
        self.tableView.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    #TODO
    def paintEvent(self, a0: QPaintEvent) -> None:
        self.lcdTime.display(time.strftime("%I" + ":" + "%M"))
        super().paintEvent(a0)

    #TODO
    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.initHeaderVertical()
        self.initHeaderHorizontal()
        super().resizeEvent(a0)
