from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
from PyQt5.uic import loadUi



#Semi-Auto Button Widget
class SemiAutoWidget(QWidget):

    def __init__(self, uipath):
        super().__init__()
        self.UIPath = uipath
        self.initUI()
        self.carPanelList = [None] * 45

    def initUI(self):
        self.ui = loadUi(self.UIPath, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(), QApplication.desktop().availableGeometry()))


