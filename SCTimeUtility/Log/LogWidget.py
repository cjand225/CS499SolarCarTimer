"""

    Module:

    Purpose:
    Depends On:

"""

import logging

from PyQt5.QtWidgets import QWidget, QStyle, QApplication, QPlainTextEdit, QTabWidget, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi

from SCTimeUtility.Log import resource_path, defaultLogFormat
from SCTimeUtility.Log.Log import get_log
from SCTimeUtility.Log.LogFilters import InfoFilter, DebugFilter, CriticalFilter, WarningFilter, ErrorFilter


class LogWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # create widget UI and add new widgets
        self.init_widget()
        self.format = None

        # get Log
        self.log = get_log()
        self.filter_list = [InfoFilter, DebugFilter, WarningFilter, ErrorFilter, CriticalFilter]
        self.filter_tab_names = ['Info', 'Debug', 'Warning', 'Error', 'Critical']
        self.handler_amount = len(self.filter_tab_names)
        self.log_handler_list = [] * self.handler_amount

        # create QTabWidget and lists for dynamically creating handlers
        self.tab_widget = QTabWidget()
        self.tab_lists = [] * self.handler_amount
        self.tab_layouts = [] * self.handler_amount

        # create tabs, add to tabwidget, add tabwidget to logWidget
        self.init_tabs()
        self.widget.logLayout.addWidget(self.tab_widget)

    '''  
        Function: initUI
        Parameters: self
        Return Value: N/A
        Purpose: Initializes, Loads and Adds UI components to LogWidget.
    '''

    def init_widget(self):
        self.widget = loadUi(resource_path, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignBottom,
                                            self.size(), QApplication.desktop().availableGeometry()))

    '''  
        Function: setFormat
        Parameters: self format
        Return Value: N/A
        Purpose: Changes the format in which log message records are displayed.
    '''

    def init_tabs(self):
        # iterate through the amount of possible filters for log and add to widget
        for x in range(0, self.handler_amount):
            handler = QTextEditLogger(self)
            handler.setFormatter(defaultLogFormat)
            handler.addFilter(self.filter_list[x]())
            self.log.addHandler(handler)

            # create a tab and its layout, add it to the tab widget
            tab = QWidget()
            self.tab_widget.addTab(tab, self.filter_tab_names[x])
            tab_layout = QGridLayout(tab)

            tab.setLayout(tab_layout)
            tab_layout.addWidget(handler.widget)

            # add the recently created objects to a list in case of need later.
            self.log_handler_list.append(handler)
            self.tab_lists.append(tab)
            self.tab_layouts.append(tab_layout)

    '''  
        Function: setFormat
        Parameters: self format
        Return Value: N/A
        Purpose: Changes the format in which log message records are displayed.
    '''

    def set_format(self, format_chosen):
        self.format = format_chosen
        for x in range(0, self.handler_amount):
            self.log_handler_list[x].setFormatter(self.format)


class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    '''  
        Function: emit
        Parameters: self, record
        Return Value: N/A
        Purpose: Emits records that can be attached and filtered via filtering classes.
    '''

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)
