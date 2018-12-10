from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
from PyQt5.Qt import *
from SCTimeUtility.log.Log import getInfoLog, getCriticalLog, getDebugLog, getErrorLog, getWarningLog


class LeaderBoardWidget(QWidget):

    def __init__(self, uiPath):
        super().__init__()
        self.initialWidth = None
        self.ui = None
        self.uiPath = uiPath
        self.initUI()
        #self.show()
        #self.initialWidth = self.width()
        self.tableView.horizontalHeader().sectionResized.connect(self.columnResized)
        self.columnSizes = []

    def show(self):
        super().show()
        if not self.initialWidth:
            self.initialWidth = self.width()
        #print(self.initialWidth)
        self.tableView.horizontalHeader().blockSignals(True)
        self.fixHeaders()
        self.tableView.horizontalHeader().blockSignals(False)

    def columnResized(self,i,oldSize,newSize):
        # print("{0}/{1}".format(i,len(self.tableView.horizontalHeader())-1))
        #self.tableView.horizontalHeader().sectionResized.disconnect(self.columnResized)
        self.tableView.horizontalHeader().blockSignals(True)
        actual_length = self.tableView.horizontalHeader().width()
        total_length = self.tableView.horizontalHeader().length()
        #print("{0}-{1}".format(actual_length,total_length))
        if total_length!=actual_length:
            if i<len(self.tableView.horizontalHeader())-1:
                #print("{0}<={1}".format(i,len(self.tableView.horizontalHeader())-1))
                # print("Long!")
                next_size = self.tableView.horizontalHeader().sectionSize(i+1)
                # if next_size > (total_length-actual_length):
                self.tableView.horizontalHeader().resizeSection(i+1,next_size-(newSize-oldSize))
            else:
                # print("Maintain")
                self.tableView.horizontalHeader().resizeSection(i,oldSize)
        else:
            #print("Maintain")
            self.tableView.horizontalHeader().resizeSection(i,max(0,oldSize-10))
        self.tableView.horizontalHeader().blockSignals(False)
        #self.tableView.horizontalHeader().sectionResized.connect(self.columnResized)

    def initUI(self):
        self.ui = loadUi(self.uiPath, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(), QApplication.desktop().availableGeometry()))

    def fixHeaders(self,update=False):
        #print("fix headers")
        self.initHeaderHorizontal(update)
        self.initHeaderVertical()
        
    def resizeEvent(self, a0: QResizeEvent):
        if (not self.initialWidth) or (a0.size().width() > self.initialWidth):
            self.tableView.horizontalHeader().blockSignals(True)
            self.fixHeaders()
            self.tableView.horizontalHeader().blockSignals(False)

    def initHeaderHorizontal(self,update=False):
        # Resizes the horizontal header so that the table fits initially without scrollbars.
        if update:
            self.tableView.horizontalHeader().blockSignals(True)
            self.columnSizes = []
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for headerIndex in range(len(self.tableView.horizontalHeader())):
            # sectionSize computes the width of the column header.
            # As a side effect, it also forces the header to resize to f it its container.
            columnSize = self.tableView.horizontalHeader().sectionSize(headerIndex)
            if update:
                self.columnSizes.append(columnSize)
        # self.tableView.horizontalHeader()
        # self.tableView.horizontalHeader().setMinimumSectionSize(minSize)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        if update:
            self.tableView.horizontalHeader().blockSignals(False)
        

    def initHeaderVertical(self):
        # Resizes the vertical header so that the table fits initially without scrollbars.
        self.tableView.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for headerIndex in range(len(self.tableView.verticalHeader())):
            # sectionSize computes the height of the row header.
            # As a side effect, it also forces the header to resize to fit its container.
            self.tableView.verticalHeader().sectionSize(headerIndex)
        self.tableView.verticalHeader().setSectionResizeMode(QHeaderView.Interactive)
