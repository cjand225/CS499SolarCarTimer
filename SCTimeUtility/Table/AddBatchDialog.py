"""

    Module: AddBatchDialog
    Purpose: QDialog class used to import batches of cars into the main application.
    Depends On: QDialog, PyQt, logging,

"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QErrorMessage, QStyle
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.uic import loadUi

from SCTimeUtility.Log.Log import get_log


class AddBatchDialog(QDialog):

    def __init__(self, resource_path):
        super().__init__()
        self.resource_path = resource_path

        self.data = None
        self.widget = None
        self.regular_expression_validator = None
        self.validation_error = None
        self.car_list = []

        self.init_widget()
        self.init_validation()

    """
          Function: initUI
          Parameters: self
          Return Value: N/A
          Purpose: Initializes the Batch Dialog's UI which is loaded from a resource file.

    """

    def init_widget(self):
        self.widget = loadUi(self.resource_path, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(), QApplication.desktop().availableGeometry()))

    """
          Function: initValidation
          Parameters: self
          Return Value: N/A
          Purpose: Function that initializes the validators that check what data is entered within
                   the dialog.

    """

    def init_validation(self):
        self.setModal(True)
        self.regular_expression_validator = QRegExpValidator(self)
        #        self.batchEdit.setValidator(self.regValid)
        self.validation_error = QErrorMessage(self)

    """
          Function: createList
          Parameters: self
          Return Value: N/A
          Purpose: Function that parses user input for Cars to create, splitting input by newlines
                    (1 car per line) and splitting each line by commas (2 items to enter per car), 
                    anything that is malformed is thrown out and the rest is put into a list to
                    be retrieved later.

    """

    def create_list(self):
        car_batch_list = []
        self.data = self.batchEdit.toPlainText()
        for line in self.data.split('\n'):
            car_batch_list.append(line)

        # use 2d dict to split tokens by ',', if no tokens found or too many, line is skipped
        for item in car_batch_list:
            if item.count(',') == 1:
                newItemOne, newItemTwo = item.split(',')
                tempList = [newItemOne, newItemTwo]
                if tempList[0] != '' and tempList[1] != '':
                    self.car_list.append(tempList)

    """
          Function: getList
          Parameters: self
          Return Value: self.carList
          Purpose: Function that returns the list of the dialog after user has input information.

    """

    def get_list(self):
        return self.car_list

    """
          Function: clear
          Parameters: self
          Return Value: N/A
          Purpose: cleans up input from previous user input entry. (will be replaced later)

    """

    def clear_batch(self):
        self.batchEdit.clear()
        self.car_list = []

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
                self.create_list()
            else:
                super().done(r)
        else:
            super().done(r)
