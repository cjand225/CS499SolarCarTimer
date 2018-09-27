import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class table(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Time Table'                           #default name

        self.left = 0                                       #default size for table
        self.top = 0
        self.width = 1080
        self.height = 720

        self.rows = 50                                      #default values for rows/cols
        self.cols = 20

        self.createTable()                                  # creates and initializes actual table

        self.hBar = self.tableWidget.horizontalScrollBar()  #links resize col function with horizontal scroll bar
        self.hBarLastVal = self.hBar.value()
        self.hBar.valueChanged.connect(self.ColRefactor)

        self.vBar = self.tableWidget.verticalScrollBar()    #links resize row function with vertical scroll bar
        self.vBarLastVal = self.vBar.value()
        self.vBar.valueChanged.connect(self.RowResize)

        self.initUI()                                       #create UI

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.layout = QVBoxLayout()                          # Add box layout, add table to box layout
        self.layout.addWidget(self.tableWidget)              # and add box layout to widget
        self.setLayout(self.layout)

        self.show()                                          # Show widget

    def createTable(self):
        self.tableWidget = QTableWidget()                    # Create table
        self.tableWidget.setRowCount(self.rows)
        self.tableWidget.setColumnCount(self.cols)

        #requires Qstringlist for setting labels
        #self.tableWidget.setHorizontalHeaderLabels("hi")
        self.tableWidget.move(0, 0)                          #default cell pointer

        self.tableWidget.doubleClicked.connect(self.on_click) #setting action response


    def RowResize(self, val):                                 #auto resizes table rows based on verticle scroll bar
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

    def ColRefactor(self, val):                                 #auto resizes table columns based on hori scroll bar
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


    @pyqtSlot()
    def on_click(self):                                         #mostly defined for testing
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())