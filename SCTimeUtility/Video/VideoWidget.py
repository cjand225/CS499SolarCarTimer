'''
Module: VideoWidget.py
Purpose: used as the view in the MVC design pattern for the Video Module.
Depends on:
'''

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QStyle
from PyQt5.uic import loadUi


class VisionWidget(QWidget):

    def __init__(self, uipath):
        super().__init__()
        self.UIPath = uipath
        self.imgCanvas = None
        self.ImgCanvasWidth = None
        self.ImgCanvasHeight = None

        self.initUI()

    def initUI(self):
        self.ui = loadUi(self.UIPath, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignVCenter,
                                            self.size(), QApplication.desktop().availableGeometry()))
        self.ImgCanvasWidth = self.imgCanvas.frameSize().width()
        self.ImgCanvasHeight = self.imgCanvas.frameSize().height()

    def getHeight(self):
        return self.ImgCanvasHeight

    def getWidth(self):
        return self.ImgCanvasWidth

    def getCanvas(self):
        return self.imgCanvas

    def getStartButton(self):
        return self.startButton

    def getStopButton(self):
        return self.stopButton

    def clearCanvas(self):
        self.imgCanvas.clear()
