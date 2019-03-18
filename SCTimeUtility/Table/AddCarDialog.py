"""

    Module: AddCarDialog
    Purpose:
    Depends On:

"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QErrorMessage, QStyle
from PyQt5.QtGui import QIntValidator
from PyQt5.uic import loadUi

from SCTimeUtility.Log.Log import getLog


class AddCarDialog(QDialog):
    def __init__(self, uipath):
        super().__init__()
        self.UIPath = uipath

        self.ui = None
        self.intValid = None
        self.validationError = None

        self._carNumber = 0

        self.initUI()
        self.initValidation()

    '''  
        Function: initUI
        Parameters: self
        Return Value: N/A
        Purpose: Initializes and loads resource file for the AddCar QDialog 
    '''

    def initUI(self):
        self.ui = loadUi(self.UIPath, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(), QApplication.desktop().availableGeometry()))

    '''  
        Function: initValidation
        Parameters: self
        Return Value: N/A
        Purpose: Initializes the components used to validate user input before retrieval. 
    '''

    def initValidation(self):
        self.setModal(True)
        self.intValid = QIntValidator(self)
        self.carNumberEdit.setValidator(self.intValid)
        self.validationError = QErrorMessage(self)

    '''  
        Function: clearText
        Parameters: self
        Return Value: N/A
        Purpose: Clears the text of each field, usually called before user invokes dialog to ensure both fields
                 are ready for user input.
    '''

    def clearText(self):
        self.carNumberEdit.clear()
        self.teamNameEdit.clear()

    '''  
        Function: carNumber
        Parameters: self
        Return Value: int (Car Number)
        Purpose: PyQt property used to store Car Number received from the input field.
    '''

    @property
    def carNumber(self):
        try:
            return int(self.carNumberEdit.text())
        except:
            raise ValueError('{0} is not a valid number'.format(self.carNumberEdit.text()))

    '''  
        Function: teamName
        Parameters: self
        Return Value: string
        Purpose: PyQt property used to store Team Name received from the input field.
    '''

    @property
    def teamName(self):
        return self.teamNameEdit.text()

    '''  
        Function: done
        Parameters: self, r
        Return Value: N/A
        Purpose: Overloaded PyQt function specific to completed dialog, does a validation check on submission and 
                 shows a validation error if anything is incorrect, missing, or empty.
    '''

    def done(self, r):
        if r == QDialog.Accepted:
            if self.carNumberEdit.text():
                if self.teamNameEdit.text():
                    super().done(r)
                else:
                    self.validationError.showMessage("Please enter a value for {0}.".format(self.teamNameLabel.text()))
            else:
                self.validationError.showMessage("Please enter a value for {0}.".format(self.carNumberLabel.text()))
        else:
            super().done(r)

    def showValidationUser(self):
        pass
