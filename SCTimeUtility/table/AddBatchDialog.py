from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QErrorMessage, QStyle
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.uic import loadUi
from SCTimeUtility.log.Log import getLog


class AddBatchDialog(QDialog):

    def __init__(self, uipath):
        super().__init__()
        self.UIPath = uipath

        self.data = None
        self.ui = None
        self.regValid = None
        self.validationError = None
        self.carList = []

        self.initUI()
        self.initValidation()

    """
          Function: initUI
          Parameters: self
          Return Value: N/A
          Purpose: Initializes the Batch Dialog's UI which is loaded from a resource file.

    """

    def initUI(self):
        self.ui = loadUi(self.UIPath, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(), QApplication.desktop().availableGeometry()))

    """
          Function: initValidation
          Parameters: self
          Return Value: N/A
          Purpose: Function that initializes the validators that check what data is entered within
                   the dialog.

    """

    def initValidation(self):
        self.setModal(True)
        self.regValid = QRegExpValidator(self)
        #        self.batchEdit.setValidator(self.regValid)
        self.validationError = QErrorMessage(self)

    """
          Function: createList
          Parameters: self
          Return Value: N/A
          Purpose: Function that parses user input for Cars to create, splitting input by newlines
                    (1 car per line) and splitting each line by commas (2 items to enter per car), 
                    anything that is malformed is thrown out and the rest is put into a list to
                    be retrieved later.

    """

    def createList(self):
        bcList = []
        self.data = self.batchEdit.toPlainText()
        for line in self.data.split('\n'):
            bcList.append(line)

        # use 2d dict to split tokens by ',', if no tokens found or too many, line is skipped
        for item in bcList:
            if item.count(',') == 1:
                newItemOne, newItemTwo = item.split(',')
                tempList = [newItemOne, newItemTwo]
                if tempList[0] != '' and tempList[1] != '':
                    self.carList.append(tempList)

    """
          Function: getList
          Parameters: self
          Return Value: self.carList
          Purpose: Function that returns the list of the dialog after user has input information.

    """

    def getList(self):
        return self.carList

    """
          Function: clear
          Parameters: self
          Return Value: N/A
          Purpose: cleans up input from previous user input entry. (will be replaced later)

    """

    def clear(self):
        self.batchEdit.clear()
        self.carList = []

    """
          Function: done
          Parameters: self
          Return Value: N/A
          Purpose: Overridden dialog function that is called upon when user presses
                   OK/APPLY/CANCEL and makes finishes processing upon Accepted state.

    """

    def done(self, r):
        if r == QDialog.Accepted:
            if self.batchEdit.toPlainText():
                super().done(r)
                self.createList()
            else:
                super().done(r)
        else:
            super().done(r)
