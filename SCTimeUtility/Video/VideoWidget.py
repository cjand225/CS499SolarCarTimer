"""

    Module: VideoWidget
    Purpose:
    Depends On: PyQt, .ui resource file

"""

# Dependency Imports
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QStyle
from PyQt5.uic import loadUi


class VideoWidget(QWidget):
    '''

        Function: __init__
        Parameters: self, uipath
        Return Value: N/A
        Purpose:

    '''

    def __init__(self, uipath):
        super().__init__()
        self.UIPath = uipath
        self.imgCanvas = None
        self.ImgCanvasWidth = None
        self.ImgCanvasHeight = None

        self.initUI()

    '''

        Function: initUI
        Parameters: self
        Return Value: N/A
        Purpose: Constructs the ui for the widget using a resource file.

    '''

    def initUI(self):
        self.ui = loadUi(self.UIPath, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignVCenter,
                                            self.size(), QApplication.desktop().availableGeometry()))
        self.ImgCanvasWidth = self.imgCanvas.frameSize().width()
        self.ImgCanvasHeight = self.imgCanvas.frameSize().height()

    '''

        Function: getHeight
        Parameters: self
        Return Value: int
        Purpose: Returns the height of the canvas embedded within the videoWidget.

    '''

    def getHeight(self):
        return self.ImgCanvasHeight

    '''

        Function: getWidth
        Parameters: self
        Return Value: int
        Purpose: Returns the width of the canvas embedded within the videoWidget.

    '''

    def getWidth(self):
        return self.ImgCanvasWidth

    '''

        Function: getCanvas
        Parameters: self
        Return Value: QLabel
        Purpose: Returns the label of which the image canvas is made up of.

    '''

    def getCanvas(self):
        return self.imgCanvas

    '''

        Function: getStartButton
        Parameters: self
        Return Value: QPushButton
        Purpose: Returns the button that is bound to starting the camera feed.

    '''

    def getStartButton(self):
        return self.startButton

    '''

        Function: getStopButton
        Parameters: self
        Return Value: QPushButton
        Purpose: Returns the button that is bound to stopping the camera feed.

    '''

    def getStopButton(self):
        return self.stopButton

    '''

        Function: clearCanvas
        Parameters:  self
        Return Value: N/A
        Purpose: Clears the Qlabel in the widget, used to clear the image after feed has been stopped.

    '''

    def clearCanvas(self):
        self.imgCanvas.clear()
