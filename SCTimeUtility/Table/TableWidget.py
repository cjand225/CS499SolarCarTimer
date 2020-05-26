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

from SCTimeUtility.Log.Log import get_log


class TableWidget(QWidget):

    def __init__(self, resource_path):
        super().__init__()
        self.resource_path = resource_path
        self.table_view = None
        self.init_widget()
        self.save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)

    '''
        Function: initUI
        Parameters: self
        Return Value: N/A
        Purpose: Initializes the GUI for TableWidget by loading its' resource file, storing a reference to it 
                 in self.UI
                 
    '''

    def init_widget(self):
        self.widget = loadUi(self.resource_path, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter,
                                            self.size(), QApplication.desktop().availableGeometry()))
        self.lcd_time.setSegmentStyle(2)
        self.offset_edit.setTime(QTime().currentTime())
        self.show()

    '''
        Function: initHeaderHorizontal
        Parameters: self
        Return Value: N/A
        Purpose: Initializes the horizontal headers for the Table view widget, such that it has
                 proper spacing for items its displaying

    '''

    def init_horizontal_header(self):
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for headerIndex in range(len(self.table_view.horizontalHeader())):
            self.table_view.horizontalHeader().sectionSize(headerIndex)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)

    '''
        Function: iniHeaderVertical
        Parameters: self
        Return Value: N/A
        Purpose: Initializes the vertical headers for the Table view widget, such that it has
                 proper spacing for items its displaying

    '''

    def init_vertical_header(self):
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for headerIndex in range(len(self.table_view.verticalHeader())):
            self.table_view.verticalHeader().sectionSize(headerIndex)
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    # TODO
    def paintEvent(self, a0: QPaintEvent) -> None:
        self.lcd_time.display(time.strftime("%I" + ":" + "%M"))
        super().paintEvent(a0)

    # TODO
    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.init_vertical_header()
        self.init_horizontal_header()
        super().resizeEvent(a0)
