import sys
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QApplication, QStyle
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi


class Table(QWidget):

    def __init__(self):
        super().__init__()
        self.rows = None
        self.columns = None

        self.initUI()                   #create UI
        self.createTable()              # creates and initializes actual Table
        self.initVerticalScroll()       # intializes infitinite vert scrolling
        self.initHorizontalScroll()     # initializes infinite horiz scrolling

    def initUI(self):
        self.ui = loadUi('./../resources/Table.ui', self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter,
                                            self.size(), QApplication.desktop().availableGeometry()))
        self.show()

    def createTable(self):
        self.initCells()
        self.tableWidget.move(0, 0)                         #default cell pointer
        self.setActions(self.on_click)                      #set function binds

    def setActions(self, function):
        self.tableWidget.doubleClicked.connect(function)

    # takes a list of strings & interates over the list size to determine what columns are set.
    def setColumnNames(self, list):
        self.tableWidget.setHorizontalHeaderLabels(list)

    #takes a list of strings & interates over the list size to determine what rows are set.
    def setRowNames(self, list):
        self.tableWidget.setVerticalHeaderLabels(list)

    #sets cell with given string data
    def setCell(self, row, col, data):
        self.tableWidget.setItem(row, col, QTableWidgetItem(data))

    #returns contents of cell at specified location
    def getCell(self, row, col):
        return self.tableWidget.item(row, col).text()


    def getCellCount(self):
        if (self.tableWidget.columnCount() == None or self.tableWidget.rowCount() == None):
            return 0
        else:
            return self.tableWidget.columnCount() * self.tableWidget.rowCount()

    def getHorizontalHeaderItem(self, index):
        return self.tableWidget.horizontalHeaderItem(index).text()

    def getVerticalHeaderItem(self, index):
        return self.tableWidget.horizontalHeaderItem(index).text()

    #nulls out select cell
    def clearCell(self, row, col):
        self.tableWidget.setItem(row, col, None)

    #intializes cells for usage
    def initCells(self):
        blank = ""
        for col in range(self.tableWidget.columnCount()):
            for row in range(self.tableWidget.rowCount()):
                self.setCell(row, col, blank)


    #sets amount of rows
    def setRows(self, rowNum):
        self.rows = rowNum

    #sets amount of collumns
    def setColumns(self, colNum):
        self.columns = colNum

    # defines and binds vertical scroll bar to RowResize
    def initVerticalScroll(self):
        self.vBar = self.tableWidget.verticalScrollBar()    #links resize row function with vertical scroll bar
        self.vBarLastVal = self.vBar.value()
        self.vBar.valueChanged.connect(self.RowResize)

    #defines and binds horizontal scroll bar to ColumnResize
    def initHorizontalScroll(self):
        self.hBar = self.tableWidget.horizontalScrollBar()  #links resize col function with horizontal scroll bar
        self.hBarLastVal = self.hBar.value()
        self.hBar.valueChanged.connect(self.ColumnResize)


    # auto resizes Table rows based on verticle scroll bar
    def RowResize(self, val):
        bar = self.vBar
        minVal, maxVal = bar.minimum(), bar.maximum()
        avg = (minVal + maxVal) / 2
        rowCount = self.tableWidget.rowCount()

        if val > self.vBarLastVal and val >= avg:
            self.tableWidget.insertRow(rowCount)

        elif val < self.vBarLastVal:
            lastRow = rowCount - 1
            empty = True
            for col in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(lastRow, col)
                if item and item.text():
                    empty = False
                    break
                if empty:
                    self.tableWidget.removeRow(lastRow)
        self.vBarLastVal = val

    # auto resizes Table columns based on hori scroll bar
    def ColumnResize(self, val):
        bar = self.hBar
        minVal, maxVal = bar.minimum(), bar.maximum()
        avg = (minVal + maxVal) / 2
        colCount = self.tableWidget.columnCount()

        if val > self.hBarLastVal and val >= avg:
            self.tableWidget.insertColumn(colCount)

        elif val < self.hBarLastVal:
            lastCol = colCount - 1
            empty = True

            for row in range(self.tableWidget.rowCount()):
                item = self.tableWidget.item(lastCol, row)
                if item and item.text():
                    empty = False
                    break
                if empty:
                    self.tableWidget.removeColumn(lastCol)
        self.hBarLastVal = val

    def getTableWidget(self):
        return self.tableWidget

    # mostly defined for testing
    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())