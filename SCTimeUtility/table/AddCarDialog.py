from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QErrorMessage, QStyle
from PyQt5.QtGui import QIntValidator
from PyQt5.uic import loadUi
from SCTimeUtility.log.Log import getLog


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

    def initUI(self):
        self.ui = loadUi(self.UIPath, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(), QApplication.desktop().availableGeometry()))

    def initValidation(self):
        self.setModal(True)
        self.intValid = QIntValidator(self)
        self.carNumberEdit.setValidator(self.intValid)
        self.validationError = QErrorMessage(self)

    def clearText(self):
        self.carNumberEdit.clear()
        self.teamNameEdit.clear()

    @property
    def carNumber(self):
        try:
            return int(self.carNumberEdit.text())
        except:
            raise ValueError('{0} is not a valid number'.format(self.carNumberEdit.text()))

    @property
    def teamName(self):
        return self.teamNameEdit.text()

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
