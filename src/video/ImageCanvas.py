from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class ImageCanvas(QWidget):

    def __init__(self):
        super().__init__()
        self.image = None

    #sets image to be painted
    def setImage(self, image):
        self.image = image
        imageSize = image.size()
        self.setMinimumSize(imageSize)
        self.update()

    #paints image to self (QWidget)
    def paintEvent(self, paintEvent):
        canvasPainter = QPainter()
        canvasPainter.begin(self)
        if self.image:
            canvasPainter.drawImage(QPoint(0, 0), self.image)
        canvasPainter.end()
