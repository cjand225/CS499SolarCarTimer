from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QErrorMessage, QStyle
from PyQt5.QtGui import QIntValidator
from PyQt5.uic import loadUi

class AddCarDialog(QDialog):
    def __init__(self,uipath):
        super().__init__()
        self.UIPath = uipath
        self.initUI()
        self.setModal(True)
        intValidator = QIntValidator(self)
        self.carNumberEdit.setValidator(intValidator)
        self.validationError = QErrorMessage(self)
        #self.buttonBox.accepted.connect(self.validateData)
        #self.buttonBox.rejected.connect(self.reject)

    @property
    def carNumber(self):
        try:            
            return int(self.carNumberEdit.text())
        except ValueError:
            return None

    @property
    def teamName(self):
        return self.teamNameEdit.text()
    

    def done(self,r):
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
            

    def initUI(self):
        self.ui = loadUi(self.UIPath, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(), QApplication.desktop().availableGeometry()))

    # def validateData(self):
    #     try:
    #         print("GOOD: {}".format(int(self.carNumberEdit.text())))
    #         self.accept()
    #     except ValueError:
    #         error = QErrorMessage(self)
    #         error.showMessage("Invalid car number {0}!".format(self.carNumberEdit.text()))
        
        
        
