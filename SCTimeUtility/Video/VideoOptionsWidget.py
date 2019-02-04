'''
Module: VideoOptionsWidget.py
Purpose:

Depends On:
'''

from PyQt5.QtWidgets import QWidget, QStyle, QApplication
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi


class VideoOptionsWidget(QWidget):

    def __init__(self, uipath):
        super().__init__()
        self.uiPath = uipath

        self.camDevice = None
        self.deviceList = []
        self.resolution = [None, None]
        self.framesPerSecond = None

        self.initUI()

    def initUI(self):
        self.ui = loadUi(self.UIPath, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(), QApplication.desktop().availableGeometry()))

    # try opencv open to find which cameras are connected
