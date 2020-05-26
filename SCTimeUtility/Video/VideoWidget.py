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

    def __init__(self, resource_path):
        super().__init__()
        self.resource_path = resource_path
        self.img_canvas = None
        self.canvas_width = None
        self.canvas_height = None

        self.init_widget()

    '''

        Function: initUI
        Parameters: self
        Return Value: N/A
        Purpose: Constructs the ui for the widget using a resource file.

    '''

    def init_widget(self):
        self.widget = loadUi(self.resource_path, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignVCenter,
                                            self.size(), QApplication.desktop().availableGeometry()))
        self.canvas_width = self.img_canvas.frameSize().width()
        self.canvas_height = self.img_canvas.frameSize().height()

    '''

        Function: getHeight
        Parameters: self
        Return Value: int
        Purpose: Returns the height of the canvas embedded within the videoWidget.

    '''

    def get_height(self):
        return self.canvas_height

    '''

        Function: getWidth
        Parameters: self
        Return Value: int
        Purpose: Returns the width of the canvas embedded within the videoWidget.

    '''

    def get_width(self):
        return self.canvas_width

    '''

        Function: getCanvas
        Parameters: self
        Return Value: QLabel
        Purpose: Returns the label of which the image canvas is made up of.

    '''

    def get_canvas(self):
        return self.img_canvas

    '''

        Function: getStartButton
        Parameters: self
        Return Value: QPushButton
        Purpose: Returns the button that is bound to starting the camera feed.

    '''

    def get_start_button(self):
        return self.startButton

    '''

        Function: getStopButton
        Parameters: self
        Return Value: QPushButton
        Purpose: Returns the button that is bound to stopping the camera feed.

    '''

    def get_stop_button(self):
        return self.stopButton

    '''

        Function: clearCanvas
        Parameters:  self
        Return Value: N/A
        Purpose: Clears the Qlabel in the widget, used to clear the image after feed has been stopped.

    '''

    def clear_canvas(self):
        self.img_canvas.clear()
