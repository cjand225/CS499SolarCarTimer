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

    def __init__(self):
        super().__init__()


    def initUI(self):
        self.ui = loadUi('./../resources/Video.ui', self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignVCenter,
                                            self.size(), QApplication.desktop().availableGeometry()))
