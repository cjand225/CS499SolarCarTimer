from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
from PyQt5.uic import loadUi



#Semi-Auto Button Widget
class SemiAutoWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        #self.createSAWidget()
        self.carPanelList = [None] * 45
        self.createCarPanel("weee", 0)

    def initUI(self):
        self.ui = loadUi('./../resources/Buttons.ui', self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(), QApplication.desktop().availableGeometry()))


