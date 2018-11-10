'''
Module: VisionWidget.py
Purpose:
Depends on:
'''


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi


class VisionWidget(QWidget):

    def __init__(self, uipath):
        super().__init__()

        self.UIPath = uipath


    def initUI(self):
        self.ui = loadUi(self.UIPath, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignVCenter,
                                            self.size(), QApplication.desktop().availableGeometry()))
