from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QErrorMessage, QStyle, QPlainTextEdit
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.uic import loadUi
from src.log.Log import getInfoLog, getCriticalLog, getDebugLog, getErrorLog, getWarningLog


class AddBatchDialog(QDialog):

    def __init__(self, uipath):
        super().__init__()
        self.UIPath = uipath

        self.data = None
        self.carList = []

        self.initUI()
        self.initValidation()

    def initUI(self):
        self.ui = loadUi(self.UIPath, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(), QApplication.desktop().availableGeometry()))

    def initValidation(self):
        self.setModal(True)
        self.regValid = QRegExpValidator(self)
        #        self.batchEdit.setValidator(self.regValid)
        self.validationError = QErrorMessage(self)

    # creates a list from the data entered
    def createList(self):
        list = []
        self.data = self.batchEdit.toPlainText()
        for line in self.data.split('\n'):
            list.append(line)

        # use 2d dict to split tokens by ',', if no tokens found or too many, line is skipped
        for item in list:
            if item.count(',') == 1:
                newItemOne, newItemTwo = item.split(',')
                tempList = [newItemOne, newItemTwo]
                if tempList[0] != '' and tempList[1] != '':
                    self.carList.append(tempList)

    def getList(self):
        return self.carList

    def clear(self):
        self.batchEdit.clear()
        self.carList = []

    def done(self, r):
        if r == QDialog.Accepted:
            if self.batchEdit.toPlainText():
                super().done(r)
                self.createList()

            else:
                print("PH")
                # self.validationError.showMessage("Please enter a value for {0}.".format(self.teamNameLabel.text()))
        else:
            super().done(r)
