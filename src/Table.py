import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Table(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Time Table'                           #default name

        self.left = 0                                       #default size for Table
        self.top = 0
        self.width = 1080
        self.height = 700

        self.setRows(30)
        self.setColumns(30)

        self.createTable()                                  # creates and initializes actual Table
        self.initVerticalScroll()
        self.initHorizontalScroll()

        self.initUI()                                       #create UI

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter,
                                            self.size(), QApplication.desktop().availableGeometry()))
        self.resize(self.width, self.height)
        self.layout = QVBoxLayout()                          # Add box layout, add Table to box layout
        self.layout.addWidget(self.tableWidget)              # and add box layout to widget
        self.setLayout(self.layout)

        self.show()                                          # Show widget

    def createTable(self):
        self.tableWidget = QTableWidget()                    # Create Table
        self.tableWidget.setRowCount(self.rows)
        self.tableWidget.setColumnCount(self.columns)
        self.tableWidget.move(0, 0)                          #default cell pointer

        self.initCells()
        self.clearCell(1,1)

        # setting action responses
        self.tableWidget.doubleClicked.connect(self.on_click)

    #sets cell with given string data
    def setCell(self, row, col, data):
        self.tableWidget.setItem(row, col, QTableWidgetItem(data))

    #returns contents of cell at specified location
    def getCell(self, row, col):
        return self.tableWidget.item(row, col).text()

    #nulls out select cell
    def clearCell(self, row, col):
        self.tableWidget.setItem(row, col, None)

    #intializes cells for usage
    def initCells(self):
        for col in range(self.columns):
            for row in range(self.rows):
                self.setCell(row, col, "")

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
        self.hBar.valueChanged.connect(self.ColRefactor)


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
    def ColRefactor(self, val):
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

    # mostly defined for testing
    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())