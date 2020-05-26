"""

    Module:
    Purpose:
    Depends On:

"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QWidget, QApplication, QStyle, QHeaderView
from PyQt5.uic import loadUi

from SCTimeUtility.Log.Log import get_log


class LeaderBoardWidget(QWidget):

    def __init__(self, resource_path):
        super().__init__()
        self.default_widget_width = None
        self.widget = None
        self.resource_path = resource_path
        self.init_widget()

        self.column_sizes = []

    '''  
        Function: show
        Parameters: self
        Return Value: N/A
        Purpose: displays the widget as well as some initial Settings to the display.
    '''

    def show(self):
        super().show()
        if not self.default_widget_width:
            self.default_widget_width = self.width()
        self.table_view.horizontalHeader().blockSignals(True)
        self.resize_headers()
        self.table_view.horizontalHeader().blockSignals(False)

    '''  
        Function: columnResized
        Parameters: self, i, oldSize, newSize
        Return Value: N/A
        Purpose: handles resizing of columns based on the new size and previous size.
    '''

    def columnResized(self, i, oldSize, newSize):
        self.table_view.horizontalHeader().blockSignals(True)
        actual_length = self.table_view.horizontalHeader().width()
        total_length = self.table_view.horizontalHeader().length()
        if total_length != actual_length:
            if i < len(self.table_view.horizontalHeader()) - 1:
                next_size = self.table_view.horizontalHeader().sectionSize(i + 1)
                self.table_view.horizontalHeader().resizeSection(i + 1, next_size - (newSize - oldSize))
            else:
                self.table_view.horizontalHeader().resizeSection(i, oldSize)
        else:
            self.table_view.horizontalHeader().resizeSection(i, max(0, oldSize - 10))
        self.table_view.horizontalHeader().blockSignals(False)

    '''  
        Function: initUI
        Parameters: self
        Return Value: N/A
        Purpose: Initializes and loads the Resources necessary for the leaderboard widget.
    '''

    def init_widget(self):
        self.widget = loadUi(self.resource_path, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignLeft,
                                            self.size(), QApplication.desktop().availableGeometry()))
        self.table_view.horizontalHeader().sectionResized.connect(self.columnResized)

    '''  
        Function: adjustHeaders
        Parameters: self, update (default = false)
        Return Value: N/A
        Purpose: Updates headers based on sizing issues.
    '''

    def resize_headers(self, update=False):
        self.init_horizontal_header(update)
        self.init_vertical_header()

    '''  
        Function: resizeEvent
        Parameters: self, a0: QResizeEvent
        Return Value: N/A
        Purpose: Overloaded PyQt function to handle proper resizing.
    '''

    def resizeEvent(self, a0: QResizeEvent):
        if (not self.default_widget_width) or (a0.size().width() > self.default_widget_width):
            self.table_view.horizontalHeader().blockSignals(True)
            self.resize_headers()
            self.table_view.horizontalHeader().blockSignals(False)

    '''  
        Function: initHeaderHorizontal
        Parameters: self, update=False
        Return Value: N/A
        Purpose: Initializes the Settings and data needed for the headers.
    '''

    def init_horizontal_header(self, update=False):
        # Resizes the horizontal header so that the Table fits initially without scrollbars.
        if update:
            self.table_view.horizontalHeader().blockSignals(True)
            self.column_sizes = []
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for headerIndex in range(len(self.table_view.horizontalHeader())):
            # sectionSize computes the width of the column header.
            # As a side effect, it also forces the header to resize to f it its container.
            columnSize = self.table_view.horizontalHeader().sectionSize(headerIndex)
            if update:
                self.column_sizes.append(columnSize)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        if update:
            self.table_view.horizontalHeader().blockSignals(False)

    '''  
        Function: initHeaderVertical
        Parameters: self
        Return Value: N/A
        Purpose: Initializes the Settings and data needed for the headers.
    '''

    def init_vertical_header(self):
        # Resizes the vertical header so that the Table fits initially without scrollbars.
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for headerIndex in range(len(self.table_view.verticalHeader())):
            # sectionSize computes the height of the row header.
            # As a side effect, it also forces the header to resize to fit its container.
            self.table_view.verticalHeader().sectionSize(headerIndex)
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.Interactive)
