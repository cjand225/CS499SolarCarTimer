import logging

from PyQt5.QtWidgets import QWidget, QStyle, QApplication, QPlainTextEdit, QTabWidget, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi

from SCTimeUtility.Log import logUIPath, defaultLogFormat
from SCTimeUtility.Log.Log import getLog
from SCTimeUtility.Log.LogFilters import infoFilter, debugFilter, criticalFilter, warningFilter, errorFilter


class LogWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # create widget UI and add new widgets
        self.initUI()

        # get Log
        self.log = getLog()
        self.filterList = [infoFilter, debugFilter, warningFilter, errorFilter, criticalFilter]
        self.filterTabNames = ['Info', 'Debug', 'Warning', 'Error', 'Critical']
        self.handlerAmount = len(self.filterTabNames)
        self.handlerList = [] * self.handlerAmount

        # create QTabWidget and lists for dynamically creating handlers
        self.tabWidget = QTabWidget()
        self.tabsList = [] * self.handlerAmount
        self.tabLayouts = [] * self.handlerAmount

        # create tabs, add to tabwidget, add tabwidget to logWidget
        self.initTabs()
        self.ui.logLayout.addWidget(self.tabWidget)

    '''  
        Function: initUI
        Parameters: self
        Return Value: N/A
        Purpose: Initializes, Loads and Adds UI components to LogWidget.
    '''

    def initUI(self):
        self.ui = loadUi(logUIPath, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignBottom,
                                            self.size(), QApplication.desktop().availableGeometry()))

    '''  
        Function: setFormat
        Parameters: self format
        Return Value: N/A
        Purpose: Changes the format in which log message records are displayed.
    '''

    def initTabs(self):
        # iterate through the amount of possible filters for log and add to widget
        for x in range(0, self.handlerAmount):
            handler = QTextEditLogger(self)
            handler.setFormatter(defaultLogFormat)
            handler.addFilter(self.filterList[x]())
            self.log.addHandler(handler)

            # create a tab and its layout, add it to the tab widget
            tab = QWidget()
            self.tabWidget.addTab(tab, self.filterTabNames[x])
            tabLayout = QGridLayout(tab)

            tab.setLayout(tabLayout)
            tabLayout.addWidget(handler.widget)

            # add the recently created objects to a list in case of need later.
            self.handlerList.append(handler)
            self.tabsList.append(tab)
            self.tabLayouts.append(tabLayout)

    '''  
        Function: setFormat
        Parameters: self format
        Return Value: N/A
        Purpose: Changes the format in which log message records are displayed.
    '''

    def setFormat(self, format):
        self.format = format
        for x in range(0, self.handlerAmount):
            self.handlerList[x].setFormatter(self.format)


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
